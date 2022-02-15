import argparse
from datetime import datetime
from typing import Any, Dict, Iterator, List

from datadog_api_client.v1.model.point import Point
from datadog_api_client.v1.model.series import Series

from examples.common.datadog_api import DatadogApi
from examples.common.repos import ALL_REPOS, Repo, get_repos
from examples.common.sonar_cloud_api import Metrics, SonarCloudApi

METRICS = [Metrics.LINES_TO_COVER, Metrics.UNCOVERED_LINES, Metrics.BRANCH_COVERAGE]


class SonarCloudMetricCollector:
    def __init__(self, sonar_cloud_api: SonarCloudApi, datadog_api: DatadogApi):
        self.sonar_cloud_api = sonar_cloud_api
        self.datadog_api = datadog_api

    def run(self, repos: List[Repo]) -> None:
        series = []

        for repo in repos:
            measures = self.sonar_cloud_api.get_component_measures(repo.org, repo.name, METRICS)

            if measures:
                series += self.get_series(repo, measures)

        print("Series data:", series)

        self.datadog_api.submit_metrics(series)

    def get_series(self, repo: Repo, measures: List[Dict[str, Any]]) -> Iterator[Series]:
        for metric in METRICS:
            measure = next((measure for measure in measures if measure['metric'] == metric), None)

            if not measure:
                print(f'Failed to find metric "{metric}" in measures for {repo}')
                continue

            yield Series(
                metric=f'sonar_cloud.measures.{metric}',
                type='gauge',
                points=[Point([datetime.now().timestamp(), float(measure['value'])])],
                tags=[f'org:{repo.org}', f'repo:{repo.org}/{repo.name}'],
            )


def parse_args(command_args: List[str] = None) -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description='sonar-cloud-metrics')
    parser.add_argument('--org', '-o', nargs='*',
                        help='if none specified, runs on all orgs',
                        default=[],
                        choices=ALL_REPOS.keys())
    parser.add_argument('--include', '-i', nargs='*',
                        help='repos to include',
                        default=[],
                        choices=[repo.name for repo in get_repos()])
    parser.add_argument('--exclude', '-e', nargs='*',
                        help='repos to exclude',
                        default=[],
                        choices=[repo.name for repo in get_repos()])

    return vars(parser.parse_args(command_args))


if __name__ == '__main__':
    parsed_args = parse_args()

    collector = SonarCloudMetricCollector(SonarCloudApi(), DatadogApi())
    collector.run(get_repos(parsed_args['org'], parsed_args['include'], parsed_args['exclude']))
