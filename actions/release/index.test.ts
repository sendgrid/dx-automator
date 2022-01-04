import { describe, expect, jest, test } from "@jest/globals";
import * as core from "@actions/core";
import release from "./index";
import ReleaseGitHub from "./ReleaseGitHub";
import { MockedObject } from "ts-jest";

jest.mock("@actions/core");
jest.mock("./ReleaseGitHub");

const mockGetInput = core.getInput as MockedObject<any>;
const mockSetFailed = core.setFailed as MockedObject<any>;
const mockRelease = ReleaseGitHub as MockedObject<any>;

describe("release", () => {
  test("fully creates a release", async () => {
    mockGetInput.mockReturnValueOnce("CHANGES.md");
    mockGetInput.mockReturnValueOnce("**Footer**");
    mockGetInput.mockReturnValueOnce("first second third");

    await release();
    expect(mockGetInput).toHaveBeenCalledTimes(3);
    expect(mockRelease).toHaveBeenCalledTimes(1);

    const params = mockRelease.mock.calls[0][1];
    expect(params.changelogFilename).toEqual("CHANGES.md");
    expect(params.customFooter).toEqual("**Footer**");
    expect(params.assets).toEqual(["first", "second", "third"]);
  });

  test("handles no assets", async () => {
    mockGetInput.mockReturnValueOnce("CHANGES.md");
    mockGetInput.mockReturnValueOnce("**Footer**");
    mockGetInput.mockReturnValueOnce("");

    await release();

    const params = mockRelease.mock.calls[0][1];
    expect(params.assets).toEqual([]);
  });

  test("handles errors", async () => {
    mockGetInput.mockImplementation(() => {
      throw new Error("NO INPUT");
    });

    await release();
    expect(mockSetFailed).toHaveBeenCalledTimes(1);
  });
});
