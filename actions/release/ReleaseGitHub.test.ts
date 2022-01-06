import { describe, expect, jest, test } from "@jest/globals";
import ReleaseGitHub, { ReleaseGitHubParams } from "./ReleaseGitHub";
import { Context } from "@actions/github/lib/context";
import path from "path";

const CHANGES = path.join(__dirname, "fixtures", "CHANGES.md");

const mockGetReleaseByTag = jest.fn();
const mockUpdateRelease = jest.fn();
const mockCreateRelease = jest.fn();
const mockListReleaseAssets = jest.fn();
const mockDeleteReleaseAsset = jest.fn();
const mockUploadReleaseAsset = jest.fn();

jest.mock("@octokit/rest", () => ({
  Octokit: jest.fn(() => ({
    repos: {
      getReleaseByTag: mockGetReleaseByTag,
      updateRelease: mockUpdateRelease,
      createRelease: mockCreateRelease,
      listReleaseAssets: mockListReleaseAssets,
      deleteReleaseAsset: mockDeleteReleaseAsset,
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
      mockGetReleaseByTag.mockImplementation(() => {
        throw new Error("NOT FOUND");
      });
      mockCreateRelease.mockReturnValue({ data: { id: 123 } });
      mockListReleaseAssets.mockReturnValue({ data: [] });

      await release.run();
      expect(mockGetReleaseByTag).toHaveBeenCalledTimes(1);
      expect(mockCreateRelease).toHaveBeenCalledTimes(1);
      expect(mockListReleaseAssets).toHaveBeenCalledTimes(1);
      expect(mockUploadReleaseAsset).toHaveBeenCalledTimes(1);
    });
  });

  describe("release", () => {
    const release = new ReleaseGitHub(
      { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
      {} as ReleaseGitHubParams
    );

    test("creates a new release", async () => {
      mockGetReleaseByTag.mockImplementation(() => {
        throw new Error("NOT FOUND");
      });
      mockCreateRelease.mockReturnValue({ data: { id: 123 } });

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
      mockGetReleaseByTag.mockReturnValue({ data: { id: 123 } });
      mockUpdateRelease.mockReturnValue({ data: { id: 123 } });

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
  });

  describe("uploadAssets", () => {
    const release = new ReleaseGitHub(
      { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
      { assets: [CHANGES] } as ReleaseGitHubParams
    );

    test("uploads a new asset", async () => {
      mockListReleaseAssets.mockReturnValue({ data: [] });

      await release.uploadAssets(123);
      expect(mockListReleaseAssets).toHaveBeenCalledTimes(1);
      expect(mockUploadReleaseAsset).toHaveBeenCalledTimes(1);
      expect(mockDeleteReleaseAsset).not.toHaveBeenCalled();

      const params: any = mockUploadReleaseAsset.mock.calls[0][0];
      expect(params.release_id).toEqual(123);
      expect(params.name).toEqual("CHANGES.md");
    });

    test("deletes an existing asset", async () => {
      mockListReleaseAssets.mockReturnValue({
        data: [{ id: 456, name: "CHANGES.md" }],
      });

      await release.uploadAssets(123);
      expect(mockListReleaseAssets).toHaveBeenCalledTimes(1);
      expect(mockDeleteReleaseAsset).toHaveBeenCalledTimes(1);
      expect(mockUploadReleaseAsset).toHaveBeenCalledTimes(1);

      const params: any = mockDeleteReleaseAsset.mock.calls[0][0];
      expect(params.release_id).toEqual(123);
      expect(params.asset_id).toEqual(456);
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
  });

  describe("getFooter", () => {
    test("contains the Twilio footer for Twilio repos", () => {
      const release = new ReleaseGitHub(
        { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
        {} as ReleaseGitHubParams
      );
      const footer = release.getFooter("1.2.3");
      expect(footer).toHaveLength(1);
      expect(footer[0]).toContain("twilio-BASIC/1.2.3/index.html");
    });

    test("uses a different footer for twilio-go", () => {
      const release = new ReleaseGitHub(
        { repo: { owner: "twilio", repo: "twilio-go" } } as Context,
        {} as ReleaseGitHubParams
      );
      const footer = release.getFooter("1.2.3");
      expect(footer).toHaveLength(1);
      expect(footer[0]).toContain("github.com/twilio/twilio-go@1.2.3");
    });

    test("excludes the Twilio footer for non-Twilio repos", () => {
      const release = new ReleaseGitHub(
        { repo: { owner: "sendgrid", repo: "sendgrid-BASIC" } } as Context,
        {} as ReleaseGitHubParams
      );
      const footer = release.getFooter("1.2.3");
      expect(footer).toHaveLength(0);
    });

    test("includes a custom footer", () => {
      const release = new ReleaseGitHub(
        { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
        { customFooter: "this is just a test" } as ReleaseGitHubParams
      );
      const footer = release.getFooter("2021.11.12");
      expect(footer).toHaveLength(2);
      expect(footer[1]).toEqual("this is just a test");
    });

    test("expands expected variables in custom footer", () => {
      const release = new ReleaseGitHub(
        { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
        {
          customFooter: "the version is ${version}, okay",
        } as ReleaseGitHubParams
      );
      const footer = release.getFooter("1.2.3");
      expect(footer).toHaveLength(2);
      expect(footer[1]).toEqual("the version is 1.2.3, okay");
    });

    test("errors on unexpected variables in custom footer", () => {
      const release = new ReleaseGitHub(
        { repo: { owner: "twilio", repo: "twilio-BASIC" } } as Context,
        {
          customFooter: "the version is ${blur-sion}, okay",
        } as ReleaseGitHubParams
      );
      expect(() => release.getFooter("1.2.3")).toThrow("Unexpected variable");
    });
  });
});
