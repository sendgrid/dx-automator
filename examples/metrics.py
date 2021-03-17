import statistics
from collections import defaultdict
from datetime import datetime, timedelta
from functools import lru_cache
from itertools import chain
from typing import Dict, List

from common.admins import ADMINS
from common.google_api import get_spreadsheets
from common.issue import substitute, get_issues, Issue, get_delta_days, print_json, get_date_time
from common.repos import TEST_REPOS
ALL_REPOS = TEST_REPOS

GOOGLE_SHEET_ID = '1cQOOT5aYxfXOSwEV0cJyf01KkV-uKCBJnKK3PHjouCE'
GOOGLE_SHEET_NAME = 'Daily'


def base_type():
    return {'nodes': defaultdict(base_type), 'metrics': {}}


class MetricCollector:

    def __init__(self):
        self.metrics = base_type()
        self.untagged_issues = []
        self.all_metrics = []

        # Load up the spreadsheet connector early to validate credentials.
        self.spreadsheets = get_spreadsheets()

    def run(self, start_date: str, end_date: str, reporting_period: str = None) -> None:
        reporting_period = reporting_period or end_date
        global_node = self.metrics

        for org in ALL_REPOS:
            org_node = global_node['nodes'][org]

            for repo in ALL_REPOS[org]:
                repo_node = org_node['nodes'][repo]

                self.process_repo(repo_node, org, repo, start_date, end_date)

        # If we have any untagged issues, print them and exit.
        if self.untagged_issues:
            print('These issues need a "type" label:')
            for issue in self.untagged_issues:
                print(issue.url)
            return

        for org in global_node['nodes']:
            org_node = global_node['nodes'][org]

            for repo in org_node['nodes']:
                repo_node = org_node['nodes'][repo]

                self.aggregate(repo_node)
                self.summarize(repo, reporting_period, repo_node)

            self.aggregate(org_node)
            self.summarize(org, reporting_period, org_node)

        self.aggregate(global_node)
        self.summarize('global', reporting_period, global_node)

        print_json(self.metrics)

        self.output_google_sheet()

    def process_repo(self, nodes: Dict,
                     org: str, repo: str,
                     start_date: str, end_date: str) -> None:
        start_date = get_date_time(start_date)
        end_date = get_date_time(end_date)

        issues = get_repo_issues(org, repo)
        issue_count = 0
        pr_count = 0

        for issue_json in issues:
            issue = Issue(issue_json, end_date=end_date)

            if issue.author in ADMINS:
                continue

            if issue.created_at > end_date:
                continue

            issue.process_events()

            if issue.created_at >= start_date:
                issue_category = issue.get_issue_category()

                self.add_time_to_resolve(issue)

                if 'time_to_close' in issue.metrics:
                    time_to_close = issue.metrics.pop('time_to_close')

                    if issue.get_issue_status() not in ['duplicate', 'invalid']:
                        if issue.first_admin_comment:
                            if issue_category:
                                issue.metrics[f'time_to_close_{issue_category}'] = time_to_close
                            else:
                                self.untagged_issues.append(issue)

                if 'time_awaiting_resolution' in issue.metrics:
                    resolution = issue.metrics.pop('time_awaiting_resolution')

                    if issue_category:
                        issue.metrics[f'time_awaiting_resolution_{issue_category}'] = resolution
                    else:
                        self.untagged_issues.append(issue)

                if not issue.first_admin_comment:
                    issue.metrics.pop('time_to_close_pr', None)

                nodes['nodes'][issue.url]['metrics'] = issue.metrics

            if not issue.closed:
                time_open = get_delta_days(issue.created_at, end_date)

                nodes['nodes'][issue.url]['metrics']['time_open'] = time_open

                if issue.is_pr:
                    pr_count += 1
                    nodes['nodes'][issue.url]['metrics']['pr_count'] = pr_count
                else:
                    issue_count += 1
                    nodes['nodes'][issue.url]['metrics']['issue_count'] = issue_count

    def add_time_to_resolve(self, issue: Issue) -> None:
        for ext in {'', '_pr'}:
            if f'time_to_close{ext}' in issue.metrics and issue.first_admin_comment:
                contact = issue.metrics[f'time_to_contact{ext}']
                respond = issue.metrics.get(f'time_to_respond{ext}', [])
                close = issue.metrics[f'time_to_close{ext}']

                issue.metrics[f'time_to_resolve'] = sum(contact) + sum(respond) + sum(close)

    def aggregate(self, node: Dict) -> None:
        metrics: Dict[str, List[float]] = {}

        for item in node['nodes'].values():
            for metric_id, value in item['metrics'].items():
                if metric_id not in metrics:
                    metrics[metric_id] = []

                if isinstance(value, dict):
                    value = value['values']

                if not isinstance(value, list):
                    value = [value]

                metrics[metric_id].extend(value)

        for metric_id, values in metrics.items():
            node['metrics'][metric_id] = {
                'values': sorted(values),
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'mean': statistics.mean(values),
                'median': statistics.median(values),
            }

    def summarize(self, name: str, reporting_date: str, node: Dict) -> None:
        repo_metrics = {'name': name, 'date': reporting_date}

        metrics = node['metrics']

        for metric, values in metrics.items():
            for k, v in values.items():
                if k != 'values':
                    repo_metrics[f'{metric}_{k}'] = v

        self.all_metrics.append(repo_metrics)

    def output_google_sheet(self):
        response = self.spreadsheets.values().get(spreadsheetId=GOOGLE_SHEET_ID,
                                                  range=f'{GOOGLE_SHEET_NAME}!1:1').execute()
        header = response.get('values', [[]])[0]

        values = []

        for metrics in self.all_metrics:
            row = []
            values.append(row)

            for metric_id in header:
                row.append(metrics.get(metric_id))

            for metric_id, value in metrics.items():
                if metric_id not in header:
                    header.append(metric_id)
                    row.append(value)

        self.spreadsheets.values().update(spreadsheetId=GOOGLE_SHEET_ID,
                                          range=f'{GOOGLE_SHEET_NAME}!1:1',
                                          valueInputOption='USER_ENTERED',
                                          body={'values': [header]}).execute()

        self.spreadsheets.values().append(spreadsheetId=GOOGLE_SHEET_ID,
                                          range=f'{GOOGLE_SHEET_NAME}!A2:A',
                                          valueInputOption='USER_ENTERED',
                                          body={'values': values}).execute()


@lru_cache(maxsize=None)
def get_repo_issues(org: str, repo: str):
    fragment_template = """
... on %issue_type% {
    author {
        login
    }
    createdAt
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

    return list(get_issues(org, repo, ''.join(inline_fragments)))


DATE_TIME_FORMAT = '%Y-%m-%d'


def get_date_range(start_date: str, end_date: str) -> List[str]:
    start_date = datetime.strptime(start_date, DATE_TIME_FORMAT)
    end_date = datetime.strptime(end_date, DATE_TIME_FORMAT)

    while start_date <= end_date:
        yield start_date.strftime(DATE_TIME_FORMAT)
        start_date = start_date + timedelta(days=7)


def run_backfill() -> None:
    mondays = get_date_range('2020-01-06', '2020-05-18')
    fridays = get_date_range('2020-05-22', datetime.now().strftime(DATE_TIME_FORMAT))

    for end_date in chain(mondays, fridays):
        MetricCollector().run(start_date='2020-01-01',
                              end_date=end_date)


def run_today() -> None:
    today = datetime.now().strftime(DATE_TIME_FORMAT)
    MetricCollector().run(start_date=today, end_date=today)


if __name__ == '__main__':
    run_today()

    # run_backfill()

    # Q1
    # MetricCollector().run(start_date='2020-01-01',
    #                       end_date='2020-04-01',
    #                       reporting_period='2020-Q1')
