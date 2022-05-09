import * as core from "@actions/core";
import { Context } from "@actions/github/lib/context";
import {
  MetricsApi,
  MetricsApiSubmitMetricsRequest,
} from "@datadog/datadog-api-client/dist/packages/datadog-api-client-v1";
import getVersion from "../utils/getVersion";

const METRIC_TYPE_COUNT = "count";
const METRIC_TYPE_GAUGE = "gauge";
const METRIC_NAME_RELEASE_COUNT = "library.release.count";
const METRIC_NAME_RELEASE_STATUS = "library.release.status";
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

    const tags = this.getTags(this.getOrg(), this.getRepo(), this.isPreRelease());

    const release_count_params: MetricParams = {
      type: METRIC_TYPE_COUNT,
      name: METRIC_NAME_RELEASE_COUNT,
      tags: tags,
      value: 1,
    };

    const release_status_params: MetricParams = {
      type: METRIC_TYPE_GAUGE,
      name: METRIC_NAME_RELEASE_STATUS,
      tags: tags,
      value: 0, // This indicates the repo is no longer releasing. 
    };

    await Promise.all([this.sendMetric(release_count_params), this.sendMetric(release_status_params)]);
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
