import { describe, expect, jest, test } from "@jest/globals";
import DatadogReleaseMetric from "./DatadogReleaseMetric";
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

      expect(mockSubmitMetrics).toHaveBeenCalledTimes(2);
      const getMetricsRequestParams: any = mockSubmitMetrics.mock.calls;
      expect(getMetricsRequestParams.length).toEqual(2);

      for (const metricRequestParams of getMetricsRequestParams) {
        const series = metricRequestParams[0].body.series[0];
        expect(series.tags).toHaveLength(4);
        expect(series.tags).toContain("org:twilio");
        expect(series.tags).toContain("repo:twilio/twilio-BASIC");
        expect(series.tags).toContain("pre-release:false");
        expect(series.tags).toContain("type:helper");

        switch (series.metric) {
          case "library.release.count": {
            expect(series.type).toEqual("count");
            expect(series.points[0]).toContain(1);
            break;
          }

          case "library.release.status": {
            expect(series.type).toEqual("gauge");
            expect(series.points[0]).toContain(0);
            break;
          }

          default: {
            fail("Unexpected metric name");
          }
        }
      }
    });

    test("handles pre-release versions", async () => {
      const datadogReleaseMetric = new DatadogReleaseMetric(
        {
          repo: { owner: "twilio", repo: "twilio-BASIC" },
          ref: "refs/tags/1.2.3-rc1.0",
        } as Context,
        new MetricsApi({} as Configuration)
      );

      await datadogReleaseMetric.run();

      const getMetricsRequestParams: any = mockSubmitMetrics.mock.calls[0][0];
      const series = getMetricsRequestParams.body.series[0];
      expect(series.tags).toContain("pre-release:true");
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

  describe("getTags", () => {
    test("creates Datadog tags properly", () => {
      const ddReleaseMetrics = new DatadogReleaseMetric(
        {} as Context,
        {} as MetricsApi
      );

      const tags = ddReleaseMetrics.getTags("twilio", "twilio-BASIC", true);
      expect(tags).toHaveLength(4);
      expect(tags).toContain("org:twilio");
      expect(tags).toContain("repo:twilio-BASIC");
      expect(tags).toContain("pre-release:true");
      expect(tags).toContain("type:helper");
    });
  });
});
