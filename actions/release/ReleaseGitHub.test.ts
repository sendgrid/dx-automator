import { describe, expect, jest, test } from "@jest/globals";
import ReleaseGitHub, { ReleaseGitHubParams } from "./ReleaseGitHub";
import { Context } from "@actions/github/lib/context";
import path from "path";

const CHANGES = path.join(__dirname, "fixtures", "CHANGES.md");

const mockGetReleaseByTag = jest.fn();
const mockUpdateRelease = jest.fn();
const mockCreateRelease = jest.fn();
const mockUploadReleaseAsset = jest.fn();

jest.mock("@octokit/rest", () => ({
  Octokit: jest.fn(() => ({
    repos: {
      getReleaseByTag: mockGetReleaseByTag,
      updateRelease: mockUpdateRelease,
      createRelease: mockCreateRelease,
      uploadReleaseAsset: mockUploadReleaseAsset,
    },
  })),
}));

describe("ReleaseGitHub", () => {
  describe("run", () => {
    const release = new ReleaseGitHub(
      {
        repo: { owner: "twilio", repo: "twilio-BASIC" },
        ref: "refs/tags/2021.11.12",
      } as Context,
      {
        changelogFilename: CHANGES,
        assets: [CHANGES],
      } as ReleaseGitHubParams
    );

    test("fully creates a release", async () => {
      mockGetReleaseByTag.mockReturnValue({ status: 404 });
      mockCreateRelease.mockReturnValue({ status: 201, data: { id: 123 } });
      mockUploadReleaseAsset.mockReturnValue({ status: 201 });

      await release.run();
      expect(mockGetReleaseByTag).toHaveBeenCalledTimes(1);
      expect(mockCreateRelease).toHaveBeenCalledTimes(1);
      expect(mockUploadReleaseAsset).toHaveBeenCalledTimes(1);
    });
  });

  describe("release", () => {
    const release = new ReleaseGitHub(
      { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
      {} as ReleaseGitHubParams
    );

    test("creates a new release", async () => {
      mockGetReleaseByTag.mockReturnValue({ status: 404 });
      mockCreateRelease.mockReturnValue({ status: 201, data: { id: 123 } });

      const releaseId = await release.release("1.2.3", "NOTES");
      expect(releaseId).toEqual(123);
      expect(mockGetReleaseByTag).toHaveBeenCalledTimes(1);
      expect(mockCreateRelease).toHaveBeenCalledTimes(1);
      expect(mockUpdateRelease).not.toHaveBeenCalled();

      const getReleaseParams: any = mockGetReleaseByTag.mock.calls[0][0];
      expect(getReleaseParams.tag).toEqual("1.2.3");

      const createReleaseParams: any = mockCreateRelease.mock.calls[0][0];
      expect(createReleaseParams.tag_name).toEqual("1.2.3");
      expect(createReleaseParams.name).toEqual("1.2.3");
      expect(createReleaseParams.body).toEqual("NOTES");
    });

    test("updates an existing release", async () => {
      mockGetReleaseByTag.mockReturnValue({ status: 200, data: { id: 123 } });
      mockUpdateRelease.mockReturnValue({ status: 200, data: { id: 123 } });

      const releaseId = await release.release("1.2.3", "NOTES");
      expect(releaseId).toEqual(123);
      expect(mockGetReleaseByTag).toHaveBeenCalledTimes(1);
      expect(mockUpdateRelease).toHaveBeenCalledTimes(1);
      expect(mockCreateRelease).not.toHaveBeenCalled();

      const updateReleaseParams: any = mockUpdateRelease.mock.calls[0][0];
      expect(updateReleaseParams.release_id).toEqual(123);
      expect(updateReleaseParams.tag_name).toEqual("1.2.3");
      expect(updateReleaseParams.name).toEqual("1.2.3");
      expect(updateReleaseParams.body).toEqual("NOTES");
    });

    test("handles create release API failures", async () => {
      mockGetReleaseByTag.mockReturnValue({ status: 404 });
      mockCreateRelease.mockReturnValue({
        status: 500,
        data: "Internal server error",
      });

      await expect(release.release("1.2.3", "NOTES")).rejects.toThrow(
        "Unable to create"
      );
    });

    test("handles update release API failures", async () => {
      mockGetReleaseByTag.mockReturnValue({ status: 200, data: { id: 123 } });
      mockUpdateRelease.mockReturnValue({
        status: 500,
        data: "Internal server error",
      });

      await expect(release.release("1.2.3", "NOTES")).rejects.toThrow(
        "Unable to update"
      );
    });
  });

  describe("uploadAssets", () => {
    const release = new ReleaseGitHub(
      { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
      { assets: [CHANGES] } as ReleaseGitHubParams
    );

    test("uploads the asset", async () => {
      mockUploadReleaseAsset.mockReturnValue({ status: 201 });

      await release.uploadAssets(123);
      expect(mockUploadReleaseAsset).toHaveBeenCalledTimes(1);

      const params: any = mockUploadReleaseAsset.mock.calls[0][0];
      expect(params.release_id).toEqual(123);
      expect(params.name).toEqual("CHANGES.md");
    });

    test("handles API failures", async () => {
      mockUploadReleaseAsset.mockReturnValue({
        status: 500,
        data: "Internal server error",
      });

      await expect(release.uploadAssets(123)).rejects.toThrow();
      expect(mockUploadReleaseAsset).toHaveBeenCalledTimes(1);
    });
  });

  describe("getVersion", () => {
    test("parses a tag ref properly", () => {
      const release = new ReleaseGitHub(
        { ref: "refs/tags/1.2.3" } as Context,
        {} as ReleaseGitHubParams
      );

      const version = release.getVersion();
      expect(version).toEqual("1.2.3");
    });

    test("throws on branch refs", () => {
      const release = new ReleaseGitHub(
        { ref: "refs/heads/main" } as Context,
        {} as ReleaseGitHubParams
      );

      expect(() => release.getVersion()).toThrow("Invalid ref");
    });

    test("throws on bad refs", () => {
      const release = new ReleaseGitHub(
        { ref: "bad-ref" } as Context,
        {} as ReleaseGitHubParams
      );

      expect(() => release.getVersion()).toThrow("Invalid ref");
    });
  });

  describe("getReleaseNotes", () => {
    const release = new ReleaseGitHub(
      { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
      {
        changelogFilename: CHANGES,
      } as ReleaseGitHubParams
    );

    test("handles the newest release", () => {
      const releaseNotes = release.getReleaseNotes("2021.11.12");
      expect(releaseNotes).toContain("Added widget");
      expect(releaseNotes).toContain("Updated docs");
      expect(releaseNotes).toContain("twilio-BASIC/2021.11.12/index.html");
      expect(releaseNotes).not.toContain("Added new thing");
      expect(releaseNotes).not.toContain("2021.1.1");
    });

    test("handles the oldest release", () => {
      const releaseNotes = release.getReleaseNotes("2021.1.1");
      expect(releaseNotes).toContain("Added new thing");
      expect(releaseNotes).toContain("Removed old thing");
      expect(releaseNotes).not.toContain("Updated docs");
    });

    test("handles long (golang) versions", () => {
      const releaseNotes = release.getReleaseNotes("v2021.11.12");
      expect(releaseNotes).toContain("Release Notes");
    });

    test("throws when the version is not found", () => {
      expect(() => release.getReleaseNotes("2021.10.11")).toThrow(
        "not found in changelog"
      );
    });

    test("excludes the footer for non-Twilio repos", () => {
      const release = new ReleaseGitHub(
        { repo: { owner: "sendgrid", repo: "sendgrid-BASIC" } } as Context,
        {
          changelogFilename: CHANGES,
        } as ReleaseGitHubParams
      );
      const releaseNotes = release.getReleaseNotes("2021.11.12");
      expect(releaseNotes).not.toContain("twilio.com");
    });

    test("includes a custom footer", () => {
      const release = new ReleaseGitHub(
        { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
        {
          changelogFilename: CHANGES,
          customFooter: "this is just a test",
        } as ReleaseGitHubParams
      );
      const releaseNotes = release.getReleaseNotes("2021.11.12");
      expect(releaseNotes).toContain("\nthis is just a test");
    });
  });
});
