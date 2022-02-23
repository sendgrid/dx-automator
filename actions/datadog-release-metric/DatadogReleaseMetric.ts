import * as core from "@actions/core";
import { Context } from "@actions/github/lib/context";
import {
  MetricsApi,
  MetricsApiSubmitMetricsRequest,
} from "@datadog/datadog-api-client/dist/packages/datadog-api-client-v1";

const METRIC_TYPE = "count";
const METRIC_NAME = "library.release.count";
const REF_REGEX = /^refs\/(.+?)\/(.+)$/;

export interface MetricParams {
  type: string;
  name: string;
  value: number;
  tags: string[];
}

export default class DatadogReleaseMetric {
  private readonly type: string = METRIC_TYPE;
  private readonly name: string = METRIC_NAME;

  constructor(private readonly context: Context, private datadog: MetricsApi) {}

  async run() {
    const params: MetricParams = {
      type: this.getType(),
      name: this.getName(),
      tags: this.getTags(this.getOrg(), this.getRepo(), this.getVersion()),
      value: 1,
    };
    await this.sendMetric(params);
  }

  getVersion(): string {
    const [ref, refType, refName] = this.context.ref.match(REF_REGEX) || [];

    if (!ref) {
      throw new Error(`Invalid ref: ${this.context.ref}`);
    }
    if (refType !== "tags") {
      throw new Error(`Invalid ref type, must be "tags": ${refType}`);
    }

    return refName;
  }

  getTags(owner: string, repo: string, version: string): string[] {
    return [
      `org:${owner}`,
      `repo:${repo}`,
      "type:helper",
      `version:${version}`,
    ];
  }

  private getOrg(): string {
    return this.context.repo.owner;
  }

  private getRepo(): string {
    return `${this.context.repo.owner}/${this.context.repo.repo}`;
  }

  getType(): string {
    return this.type;
  }

  getName(): string {
    return this.name;
  }

  async sendMetric(metricParams: MetricParams): Promise<void> {
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
