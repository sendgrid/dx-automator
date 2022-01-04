import * as core from "@actions/core";
import * as github from "@actions/github";
import ReleaseGitHub from "./ReleaseGitHub";

const main = async () => {
  try {
    const changelogFilename = core.getInput("changelog-filename");
    const customFooter = core.getInput("footer");
    const assetsString = core.getInput("assets");

    const assets = assetsString ? assetsString.split(" ") : [];

    await new ReleaseGitHub(github.context, {
      changelogFilename,
      customFooter,
      assets,
    }).run();
  } catch (error) {
    if (error instanceof Error) {
      core.setFailed(error.message);
    }
  }
};

main();

export default main;
