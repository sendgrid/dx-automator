import * as core from "@actions/core";
import { Context } from "@actions/github/lib/context";
import { Octokit } from "@octokit/rest";
import { createReadStream, readFileSync, statSync } from "fs";
import * as path from "path";

const VERSION_REGEX = /\[([\d-]+)] +[vV]ersion +(\d+\.\d+\.\d+)\s?/;
const REF_REGEX = /^refs\/(.+?)\/(.+)$/;
const VARIABLE_REGEX = /\${.*?}/;
const CHANGELOG_FILENAMES = ["CHANGES.md", "CHANGELOG.md"];

export interface ReleaseGitHubParams {
  changelogFilename: string;
  customFooter: string;
  assets: string[];
}

export default class ReleaseGitHub {
  constructor(
    private readonly context: Context,
    private readonly params: ReleaseGitHubParams,
    private readonly octokit = new Octokit({ auth: process.env.GITHUB_TOKEN })
  ) {}

  async run() {
    const version = this.getVersion();
    const releaseNotes = this.getReleaseNotes(version);
    const releaseId = await this.release(version, releaseNotes);
    await this.uploadAssets(releaseId);
  }

  getVersion(): string {
    const [ref, refType, refName] = this.context.ref.match(REF_REGEX) || [];

    if (!ref) {
      throw new Error(`Invalid ref: ${this.context.ref}`);
    }
    if (refType !== "tags") {
      throw new Error(`Invalid ref type, must be "tags": ${refType}`);
    }

    return refName;
  }

  getReleaseNotes(version: string): string {
    const shortVersion = version.replace(/^\D/, "");
    const changelogLines = this.getChangelogLines();

    let start = -1;
    let end = changelogLines.length;

    core.info(`Searching for version ${shortVersion} in changelog`);

    for (const [i, line] of changelogLines.entries()) {
      if (line.match(VERSION_REGEX)) {
        if (start < 0) {
          // Find the first version heading in changelog, i.e., start
          if (line.includes(shortVersion)) {
            start = i + 2;
          }
        } else {
          // Find the second version heading in changelog, i.e., end
          end = i;
          break;
        }
      }
    }

    if (start < 0) {
      throw new Error(`Version ${shortVersion} not found in changelog`);
    }

    return [
      ...this.getHeader(),
      "**Release Notes**",
      "------------",
      ...changelogLines.slice(start, end),
      ...this.getFooter(version),
    ].join("\n");
  }

  async release(version: string, releaseNotes: string): Promise<number> {
    let existingRelease;

    try {
      existingRelease = await this.octokit.repos.getReleaseByTag({
        ...this.context.repo,
        tag: version,
      });
    } catch (error) {
      core.info(`Could not get existing GitHub release: ${error}`);
    }

    if (existingRelease) {
      core.info(`Updating existing GitHub release: ${version}`);
      const updateReleaseResponse = await this.octokit.repos.updateRelease({
        ...this.context.repo,
        release_id: existingRelease.data.id,
        tag_name: version,
        name: version,
        body: releaseNotes,
      });

      return updateReleaseResponse.data.id;
    } else {
      core.info(`Creating GitHub release: ${version}`);
      const createReleaseResponse = await this.octokit.repos.createRelease({
        ...this.context.repo,
        tag_name: version,
        name: version,
        body: releaseNotes,
      });

      return createReleaseResponse.data.id;
    }
  }

  async uploadAssets(releaseId: number): Promise<void> {
    const assetsResponse = await this.octokit.repos.listReleaseAssets({
      ...this.context.repo,
      release_id: releaseId,
    });

    for (const asset of assetsResponse.data) {
      core.info(
        `Deleting GitHub release asset: id=${asset.id}, name=${asset.name}`
      );
      await this.octokit.repos.deleteReleaseAsset({
        ...this.context.repo,
        release_id: releaseId,
        asset_id: asset.id,
      });
    }

    for (const asset of this.params.assets) {
      core.info(`Reading asset from disk: ${asset}`);
      const assetContents = createReadStream(asset) as any;
      const assetSize = statSync(asset).size;
      const assetName = path.basename(asset);

      core.info(`Uploading GitHub release asset: ${asset}`);
      await this.octokit.repos.uploadReleaseAsset({
        ...this.context.repo,
        release_id: releaseId,
        name: assetName,
        data: assetContents,
        headers: {
          "Content-Type": "application/zip",
          "Content-Length": assetSize,
        },
      });
    }
  }

  getChangelogLines(): string[] {
    const changelogFilenames = this.params.changelogFilename
      ? [this.params.changelogFilename]
      : CHANGELOG_FILENAMES;

    for (const filename of changelogFilenames) {
      try {
        core.info(`Attempting to read changelog: ${filename}`);
        const changelog = readFileSync(filename, "utf-8");
        return changelog.split("\n");
      } catch (error) {
        core.info(`Failed reading changelog: ${filename}`);
      }
    }

    throw new Error("Failed to find a changelog file");
  }

  getHeader(): string[] {
    return [];
  }

  getFooter(version: string): string[] {
    let footer: string[] = [];

    if (this.context.repo.owner === "twilio") {
      if (this.context.repo.repo === "twilio-go") {
        footer = [
          `**[Docs](https://pkg.go.dev/github.com/${this.context.repo.owner}/${this.context.repo.repo}@${version})**`,
        ];
      } else {
        footer = [
          `**[Docs](https://twilio.com/docs/libraries/reference/${this.context.repo.repo}/${version}/index.html)**`,
        ];
      }
    }

    if (this.params.customFooter) {
      let expandedFooter = this.params.customFooter;

      const expectedVariables = { version: version };
      Object.entries(expectedVariables).forEach(([key, value]) => {
        expandedFooter = expandedFooter.replace(`\${${key}}`, value);
      });

      const [unexpected] = expandedFooter.match(VARIABLE_REGEX) || [];
      if (unexpected) {
        throw new Error(`Unexpected variable in footer: ${unexpected}`);
      }

      footer = footer.concat(expandedFooter.split("\n"));
    }

    return footer;
  }
}
