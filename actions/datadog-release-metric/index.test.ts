import { describe, expect, jest, test } from "@jest/globals";
import * as core from "@actions/core";
import { v1 } from "@datadog/datadog-api-client";
import datadogReleaseMetric from "./index";
import DatadogReleaseMetric from "./DatadogReleaseMetric";
import { MockedObject } from "ts-jest";

jest.mock("@actions/core");
jest.mock("@actions/github");
jest.mock("@datadog/datadog-api-client");
jest.mock("./DatadogReleaseMetric");

const mockSetFailed = core.setFailed as MockedObject<any>;
const mockDatadogReleaseMetric = DatadogReleaseMetric as MockedObject<any>;
const mockCreateConfiguration = v1.createConfiguration as MockedObject<any>;
const mockDatadogMetricsApi = v1.MetricsApi as MockedObject<any>;

describe("datadog-release-metric", () => {
  const OLD_ENV = process.env;

  beforeEach(() => {
    jest.resetModules();
    process.env = { ...OLD_ENV };
  });

  afterAll(() => {
    process.env = OLD_ENV;
  });

  test("submits a datadog release metric", async () => {
    process.env.DD_API_KEY = "api-key";

    await datadogReleaseMetric();
    expect(mockDatadogReleaseMetric).toHaveBeenCalledTimes(1);
    expect(mockCreateConfiguration).toHaveBeenCalledTimes(1);
    expect(mockDatadogMetricsApi).toHaveBeenCalledTimes(1);
  });

  test("handles errors", async () => {
    await datadogReleaseMetric();
    expect(mockCreateConfiguration).toHaveBeenCalledTimes(0);
    expect(mockDatadogMetricsApi).toHaveBeenCalledTimes(0);
    expect(mockSetFailed).toHaveBeenCalledTimes(1);
  });
});
