import * as core from "@actions/core";
import { Context } from "@actions/github/lib/context";
import {
  MetricsApi,
  MetricsApiSubmitMetricsRequest,
} from "@datadog/datadog-api-client/dist/packages/datadog-api-client-v1";
import getVersion from "../utils/getVersion";

const METRIC_TYPE = "count";
const METRIC_NAME = "library.release.count";
const PRE_RELEASE_SEPARATOR = "-";

export interface MetricParams {
  type: string;
  name: string;
  value: number;
  tags: string[];
}

export default class DatadogReleaseMetric {
  constructor(private readonly context: Context, private datadog: MetricsApi) {}

  async run() {
    if (!this.isTaggedCommit()) {
      throw new Error("This GitHub Action should only be run on tags");
    }

    const params: MetricParams = {
      type: METRIC_TYPE,
      name: METRIC_NAME,
      tags: this.getTags(this.getOrg(), this.getRepo(), this.isPreRelease()),
      value: 1,
    };
    await this.sendMetric(params);
  }

  getTags(org: string, repo: string, isPreRelease: boolean): string[] {
    return [
      `org:${org}`,
      `repo:${repo}`,
      `pre-release:${isPreRelease}`,
      "type:helper",
    ];
  }

  private isTaggedCommit(): boolean {
    try {
      const version = this.getVersion();
      return !!version;
    } catch (error) {
      return false;
    }
  }

  private getOrg(): string {
    return this.context.repo.owner;
  }

  private getRepo(): string {
    return `${this.context.repo.owner}/${this.context.repo.repo}`;
  }

  private getVersion(): string {
    return getVersion(this.context);
  }

  private isPreRelease(): boolean {
    return this.getVersion().includes(PRE_RELEASE_SEPARATOR);
  }

  private async sendMetric(metricParams: MetricParams): Promise<void> {
    core.info(`Submitting Datadog Metric: ${metricParams.name}`);
    const params: MetricsApiSubmitMetricsRequest = {
      body: {
        series: [
          {
            metric: metricParams.name,
            type: metricParams.type,
            tags: metricParams.tags,
            points: [[new Date().getTime() / 1000, metricParams.value]],
          },
        ],
      },
    };

    await this.datadog.submitMetrics(params);
  }
}
