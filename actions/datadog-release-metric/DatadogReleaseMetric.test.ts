import { describe, expect, jest, test } from "@jest/globals";
import DatadogReleaseMetric, { MetricParams } from "./DatadogReleaseMetric";
import { Context } from "@actions/github/lib/context";
import {
  Configuration,
  MetricsApi,
} from "@datadog/datadog-api-client/dist/packages/datadog-api-client-v1";

const mockSubmitMetrics = jest.spyOn(MetricsApi.prototype, "submitMetrics");

describe("DatadogReleaseMetric", () => {
  const OLD_ENV = process.env;

  beforeAll(() => {
    jest.resetModules();
    process.env = {
      ...OLD_ENV,
      DD_API_KEY: "api-key",
    };
  });

  beforeEach(() => {
    jest.clearAllMocks();
  });

  afterAll(() => {
    process.env = OLD_ENV;
  });

  describe("run", () => {
    test("fully submits a Datadog Metric", async () => {
      const datadogReleaseMetric = new DatadogReleaseMetric(
        {
          repo: { owner: "twilio", repo: "twilio-BASIC" },
          ref: "refs/tags/1.2.3",
        } as Context,
        new MetricsApi({} as Configuration)
      );

      await datadogReleaseMetric.run();

      expect(mockSubmitMetrics).toHaveBeenCalledTimes(1);
      const getMetricsRequestParams: any = mockSubmitMetrics.mock.calls[0][0];
      expect(getMetricsRequestParams.body.series[0].metric).toEqual(
        "library.release.count"
      );
      expect(getMetricsRequestParams.body.series[0].type).toEqual("count");
      expect(getMetricsRequestParams.body.series[0].tags).toHaveLength(3);
      expect(getMetricsRequestParams.body.series[0].tags).toContain(
        "org:twilio"
      );
      expect(getMetricsRequestParams.body.series[0].tags).toContain(
        "repo:twilio/twilio-BASIC"
      );
      expect(getMetricsRequestParams.body.series[0].tags).toContain(
        "type:helper"
      );
      expect(getMetricsRequestParams.body.series[0].points[0]).toContain(1);
    });

    test("errors when no tag present", async () => {
      const datadogReleaseMetric = new DatadogReleaseMetric(
        {
          repo: { owner: "twilio", repo: "twilio-BASIC" },
          ref: "refs/heads/main",
        } as Context,
        new MetricsApi({} as Configuration)
      );

      await expect(datadogReleaseMetric.run()).rejects.toThrow(
        "This GitHub Action should only be run on tags"
      );
    });
  });

  describe("sendMetric", () => {
    test("sends a metric to Datadog", async () => {
      const ddReleaseMetrics = new DatadogReleaseMetric(
        {} as Context,
        new MetricsApi({} as Configuration)
      );
      await ddReleaseMetrics.sendMetric({
        type: "count",
        name: "library.release.count",
        value: 1,
        tags: ["org:twilio", "repo:twilio/twilio-BASIC", "type:helper"],
      } as MetricParams);
      expect(mockSubmitMetrics).toHaveBeenCalledTimes(1);

      const getMetricsRequestParams: any = mockSubmitMetrics.mock.calls[0][0];
      expect(getMetricsRequestParams.body.series[0].metric).toEqual(
        "library.release.count"
      );
      expect(getMetricsRequestParams.body.series[0].type).toEqual("count");
      expect(getMetricsRequestParams.body.series[0].tags).toContain(
        "org:twilio"
      );
      expect(getMetricsRequestParams.body.series[0].tags).toContain(
        "repo:twilio/twilio-BASIC"
      );
      expect(getMetricsRequestParams.body.series[0].tags).toContain(
        "type:helper"
      );
      expect(getMetricsRequestParams.body.series[0].points[0]).toContain(1);
    });
  });

  describe("getTags", () => {
    test("creates Datadog tags properly", () => {
      const ddReleaseMetrics = new DatadogReleaseMetric(
        {} as Context,
        {} as MetricsApi
      );

      const tags = ddReleaseMetrics.getTags("twilio", "twilio-BASIC");
      expect(tags).toHaveLength(3);
      expect(tags).toContain("org:twilio");
      expect(tags).toContain("repo:twilio-BASIC");
      expect(tags).toContain("type:helper");
    });
  });
});
