import argparse
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from enum import Enum
from functools import lru_cache
from typing import Dict, List, Iterator

from datadog_api_client.v1.model.point import Point
from datadog_api_client.v1.model.series import Series

from common.admins import ADMINS
from common.datadog_api import DatadogApi
from common.git_hub_api import substitute
from common.issue import get_issues, Issue, get_delta_days, get_date_time
from common.repos import ALL_REPOS, get_repos

STALE_DAYS = 365
# Tuple to specify the metric name and type to be collected in Datadog
# Type could be 'count', 'sum', 'min' or 'max'
DATADOG_METRICS = [('issue_count', 'count'), ('pr_count', 'count'),
                   ('time_to_contact', 'count'), ('time_to_contact', 'sum'),
                   ('time_to_contact_pr', 'count'), ('time_to_contact_pr', 'sum'),
                   ('time_to_close', 'count'), ('time_to_close', 'sum'),
                   ('time_open', 'max'), ('time_open_pr', 'max'),
                   ('time_awaiting_contact', 'max'), ('time_awaiting_contact_pr', 'max'),
                   ('time_awaiting_response', 'max'), ('time_awaiting_response_pr', 'max')]


def base_type():
    return {'nodes': defaultdict(base_type), 'metrics': {}}


class DatadogSeriesType(str, Enum):
    GAUGE = 'gauge'
    COUNT = 'count'


class MetricCollector:

    def __init__(self):
        self.metrics = base_type()
        self.untagged_issues = []
        self.datadog_api = DatadogApi()

    def run(self, run_options: dict) -> None:
        repos = run_options['repos']
        start_date = run_options['start_date']
        end_date = run_options['end_date']

        print(f'repos to run the metrics on: {repos}')
        global_node = self.metrics

        for repo in repos:
            org_node = global_node['nodes'][repo.org]
            repo_node = org_node['nodes'][repo.name]

            self.process_repo(repo_node, repo.org, repo.name, start_date, end_date)

        # If we have any untagged issues, print them
        if self.untagged_issues:
            print('These issues need a "type" label:')
            for issue in self.untagged_issues:
                print(issue.url)

        # Convert data to Datadog time series
        datadog_series = []

        for org in global_node['nodes']:
            org_node = global_node['nodes'][org]
            for repo in org_node['nodes']:
                repo_node = org_node['nodes'][repo]
                self.aggregate(repo_node)
                datadog_series += self.get_series_for_datadog(repo_node, org, repo)

        # Helps with debugging in GitHub Actions logs
        print('Datadog series data:', datadog_series)

        # Submit data to Datadog
        self.datadog_api.submit_metrics(datadog_series)

    def get_series_for_datadog(self, repo_node: Dict, org: str, repo: str) -> Iterator[Series]:
        for metric_name, metric_type in DATADOG_METRICS:
            try:
                category_values = repo_node['metrics'][metric_name]
            except KeyError:
                print(f'Failed to find metric "{metric_name}" for {repo}')
                continue

            for category, values in category_values.items():
                metric_value = values[metric_type]

                yield Series(
                    metric=f'library.{metric_name}.{metric_type}',
                    type=f'{DatadogSeriesType.GAUGE}',
                    points=[Point([datetime.now().timestamp(), float(metric_value)])],
                    tags=[f'org:{org}', f'repo:{org}/{repo}', f'category:{category}', 'type:helper'],
                )

    def process_repo(self, nodes: Dict,
                     org: str, repo: str,
                     start_date: str, end_date: str) -> None:
        start_date = get_date_time(start_date)
        end_date = get_date_time(end_date)
        stale_date = datetime.now() - timedelta(days=STALE_DAYS)
        stale_date = get_date_time(stale_date.strftime(DATE_TIME_FORMAT))
        issues = get_repo_issues(org, repo, start_date=start_date, end_date=end_date)

        for issue_json in issues:
            issue = Issue(issue_json, end_date=end_date)

            if issue.author in ADMINS:
                continue

            issue.process_events()
            issue_category = issue.get_issue_category()

            issue_node = nodes['nodes'][issue.url]
            issue_node['category'] = issue_category

            if issue.created_at >= stale_date:
                self.add_time_to_resolve(issue)

                if 'time_to_close' in issue.metrics:
                    if issue.get_issue_status() in ['duplicate', 'invalid'] or not issue.first_admin_comment:
                        issue.metrics.pop('time_to_close')
                    elif not issue_category:
                        self.untagged_issues.append(issue)

                if 'time_awaiting_resolution' in issue.metrics and not issue_category:
                    self.untagged_issues.append(issue)

                if not issue.first_admin_comment:
                    issue.metrics.pop('time_to_close_pr', None)

                issue_node['metrics'] = issue.metrics

            if issue.is_open():
                time_open = get_delta_days(issue.created_at, end_date)
                if issue.is_pr:
                    issue_node['metrics']['pr_count'] = 1
                    issue_node['metrics']['time_open_pr'] = time_open
                else:
                    issue_node['metrics']['issue_count'] = 1
                    issue_node['metrics']['time_open'] = time_open

    def add_time_to_resolve(self, issue: Issue) -> None:
        for ext in {'', '_pr'}:
            if f'time_to_close{ext}' in issue.metrics and issue.first_admin_comment:
                contact = issue.metrics[f'time_to_contact{ext}']
                respond = issue.metrics.get(f'time_to_respond{ext}', [])
                close = issue.metrics[f'time_to_close{ext}']

                issue.metrics[f'time_to_resolve'] = sum(contact) + sum(respond) + sum(close)

    def aggregate(self, node: Dict) -> None:
        metrics = node['metrics']

        for item in node['nodes'].values():
            category = item['category']

            for metric_id, values in item['metrics'].items():
                if isinstance(values, dict):
                    values = values['values']
                if not isinstance(values, list):
                    values = [values]

                if metric_id not in metrics:
                    metrics[metric_id] = {}
                if category not in metrics[metric_id]:
                    metrics[metric_id][category] = {
                        'count': 0,
                        'sum': 0,
                        'min': float('inf'),
                        'max': float('-inf')
                    }

                category_metrics = metrics[metric_id][category]
                category_metrics['count'] += len(values)
                category_metrics['sum'] += sum(values)
                category_metrics['min'] = min(values + [category_metrics['min']])
                category_metrics['max'] = max(values + [category_metrics['max']])


@lru_cache(maxsize=None)
def get_repo_issues(org: str, repo: str, start_date: str, end_date: str):
    fragment_template = """
... on %issue_type% {
    author {
        login
    }
    createdAt
    closedAt
    url
    timelineItems(first: 100, itemTypes: [LABELED_EVENT UNLABELED_EVENT
                                          ISSUE_COMMENT
                                          CLOSED_EVENT REOPENED_EVENT
                                          %additional_event_names%]) {
        nodes {
            __typename
            ... on LabeledEvent {
                createdAt
                label {
                    id
                    name
                }
            }
            ... on UnlabeledEvent {
                createdAt
                label {
                    id
                    name
                }
            }
            ... on IssueComment {
                createdAt
                author {
                    login
                }
            }
            ... on ClosedEvent {
                createdAt
            }
            ... on ReopenedEvent {
                createdAt
            }
            %additional_event_types%
        }
    }
}"""

    fragment_params = [
        {
            'issue_type': 'Issue'
        },
        {
            'issue_type': 'PullRequest',
            'additional_event_names': ['PULL_REQUEST_COMMIT', 'PULL_REQUEST_REVIEW',
                                       'MERGED_EVENT'],
            'additional_event_types': [
                '... on PullRequestCommit {commit {committedDate author {user {login}} status {state} statusCheckRollup {state}}}',
                '... on PullRequestReview {createdAt state author {login}}',
                '... on MergedEvent {createdAt}']
        }
    ]

    inline_fragments = [substitute(fragment_template, fragment)
                        for fragment in fragment_params]

    return list(get_issues(org, repo, ''.join(inline_fragments),
                           start_date=start_date, end_date=end_date))


DATE_TIME_FORMAT = '%Y-%m-%d'


def run(org: List[str], include: List[str], exclude: List[str]) -> None:
    today = datetime.now().strftime(DATE_TIME_FORMAT)
    repos = get_repos(org, include, exclude)
    options = {
        'repos': repos,
        'start_date': '2020-01-01',
        'end_date': today,
    }

    MetricCollector().run(options)


def parse_args():
    parser = argparse.ArgumentParser(description='dx-automator')
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

    parsed_args = vars(parser.parse_args())

    if not parsed_args:
        parser.print_help()
        sys.exit(1)

    return parsed_args


if __name__ == '__main__':
    args = parse_args()

    run(args['org'], args['include'], args['exclude'])
