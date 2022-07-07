import * as core from "@actions/core";
import * as github from "@actions/github";
import { client, v1 } from "@datadog/datadog-api-client";
import DatadogReleaseMetric from "./DatadogReleaseMetric";

const main = async () => {
  try {
    if (!("DD_API_KEY" in process.env)) {
      throw new Error("DD_API_KEY environment variable must be set");
    }
    const config = client.createConfiguration();
    await new DatadogReleaseMetric(
      github.context,
      new v1.MetricsApi(config)
    ).run();
  } catch (error) {
    if (error instanceof Error) {
      core.setFailed(error.message);
    }
  }
};

main();

export default main;
