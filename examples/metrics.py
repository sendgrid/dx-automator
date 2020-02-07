import json
import os
import re
import statistics
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List

import requests

from examples.common.google_api import get_spreadsheets
from examples.common.repos import ALL_REPOS

ADMINS = {'childish-sambino', 'eshanholtz', 'thinkingserious'}
DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

ISSUE_TYPES = {'question', 'support', 'bug', 'enhancement', 'non-library', 'docs', 'security'}
ISSUE_STATUSES = {'duplicate', 'invalid'}

GOOGLE_SHEET_ID = '1cQOOT5aYxfXOSwEV0cJyf01KkV-uKCBJnKK3PHjouCE'


def base_type():
    return {'nodes': defaultdict(base_type), 'metrics': {}}


class MetricCollector:

    def __init__(self):
        self.metrics = base_type()
        self.all_metrics = []

    def run(self, start_date: str, end_date: str) -> None:
        global_node = self.metrics

        for org in ALL_REPOS:
            org_node = global_node['nodes'][org]

            for repo in ALL_REPOS[org]:
                repo_node = org_node['nodes'][repo]

                self.process_repo(repo_node, org, repo, start_date, end_date)

        for org in global_node['nodes']:
            org_node = global_node['nodes'][org]

            for repo in org_node['nodes']:
                repo_node = org_node['nodes'][repo]

                self.aggregate(repo_node)
                self.summarize(repo, end_date, repo_node)

            self.aggregate(org_node)
            self.summarize(org, end_date, org_node)

        self.aggregate(global_node)
        self.summarize('global', end_date, global_node)

        print_json(self.metrics)

        self.output_google_sheet()

    def process_repo(self, nodes: Dict,
                     org: str, repo: str,
                     start_date: str, end_date: str) -> None:
        start_date = get_date_time(start_date)
        end_date = get_date_time(end_date)

        for issue_json in get_issues(org, repo,
                                     start_date=start_date,
                                     end_date=end_date):
            try:
                issue = Issue(issue_json, end_date=end_date)

                if issue.author in ADMINS:
                    continue

                event_type_map = {
                    'LabeledEvent': issue.add_label,
                    'UnlabeledEvent': issue.remove_label,
                    'IssueComment': issue.comment,
                    'ClosedEvent': issue.close,
                    'ReopenedEvent': issue.reopen,
                    'PullRequestCommit': issue.commit,
                    'PullRequestReview': issue.review,
                    'MergedEvent': issue.merge,
                }

                for event in issue.events:
                    event_type = event['__typename']
                    action = event_type_map[event_type]
                    action(event)

                issue_type = issue.get_issue_type()

                if 'time_to_close' in issue.metrics:
                    issue_type = issue_type or 'unknown'
                    time_to_close = issue.metrics.pop('time_to_close')

                    if issue.get_issue_status() not in ['duplicate', 'invalid']:
                        if issue.first_admin_comment:
                            issue.metrics[f'time_to_close_{issue_type}'] = time_to_close

                if not issue.first_admin_comment:
                    issue.metrics.pop('time_to_close_pr', None)

                nodes['nodes'][issue.url]['metrics'] = issue.metrics

            except Exception as e:
                print_json(issue_json)
                raise e

        for issue_json in get_issues(org, repo,
                                     state='open',
                                     end_date=end_date):
            try:
                issue = Issue(issue_json, end_date=end_date)

                if issue.author in ADMINS:
                    continue

                time_open = get_delta_days(issue.created_at, end_date)

                nodes['nodes'][issue.url]['metrics']['time_open'] = time_open

            except Exception as e:
                print_json(issue_json)
                raise e

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
        spreadsheets = get_spreadsheets()

        response = spreadsheets.values().get(spreadsheetId=GOOGLE_SHEET_ID,
                                             range='Sheet1!1:1').execute()
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

        spreadsheets.values().update(spreadsheetId=GOOGLE_SHEET_ID,
                                     range='Sheet1!1:1',
                                     valueInputOption='USER_ENTERED',
                                     body={'values': [header]}).execute()

        spreadsheets.values().append(spreadsheetId=GOOGLE_SHEET_ID,
                                     range='Sheet1!A2:A',
                                     valueInputOption='USER_ENTERED',
                                     body={'values': values}).execute()


class Issue:
    def __init__(self, issue_json: Dict, end_date: str):
        self.end_date = end_date
        self.author = get_author(issue_json)
        self.type = issue_json['__typename']
        self.created_at = issue_json['createdAt']
        self.events = issue_json['timelineItems']['nodes']
        self.url = issue_json['url']

        self.metrics = {}
        self.labels = {}

        self.last_comment = None
        self.first_admin_comment = None
        self.last_admin_comment = None
        self.last_community_comment = None
        self.waiting_for_feedback = None
        self.waiting_removed = None
        self.type_added = None
        self.checks_passed = None
        self.closed = None
        self.merged = None

    @property
    def is_pr(self):
        return self.type == 'PullRequest'

    def add_label(self, label_event: Dict) -> None:
        label = label_event['label']

        self.labels[label['id']] = label['name']

        self.add_contact_time(self.created_at,
                              label_event['createdAt'])

        if 'waiting' in label['name'].lower():
            self.waiting_for_feedback = label_event

        if 'type:' in label['name'].lower():
            self.type_added = label_event

    def remove_label(self, label_event: Dict) -> None:
        label = label_event['label']

        # Safely remove label.
        self.labels.pop(label['id'], None)

        if 'waiting' in label['name'].lower():
            self.waiting_removed = label_event

            if self.waiting_for_feedback and self.last_community_comment:
                self.add_response_time(self.last_community_comment['createdAt'],
                                       label_event['createdAt'])
            self.waiting_for_feedback = None

    def close(self, close_event: Dict) -> None:
        self.closed = close_event

        start_time = self.created_at

        if self.waiting_removed:
            start_time = self.waiting_removed['createdAt']

        if self.type_added:
            start_time = self.type_added['createdAt']

        if self.checks_passed:
            start_time = self.checks_passed['committedDate']

        self.add_close_time(start_time,
                            close_event['createdAt'])

        # If there's no contact time yet, use the first admin comment.
        if self.first_admin_comment:
            self.add_contact_time(self.created_at,
                                  self.first_admin_comment['createdAt'])

    def reopen(self, reopen_event: Dict) -> None:
        self.closed = None

    def commit(self, commit_event: Dict) -> None:
        commit = commit_event['commit']

        if get_author(commit) not in ADMINS:
            status = commit['status'] or {}
            self.checks_passed = commit if status.get('state') == 'SUCCESS' else None
            self.waiting_for_feedback = None

    def review(self, review_event: Dict) -> None:
        if get_author(review_event) in ADMINS:
            self.comment(review_event)

            if review_event['state'] != 'APPROVED':
                self.waiting_for_feedback = review_event

    def merge(self, merge_event: Dict) -> None:
        self.merged = merge_event

    def comment(self, comment: Dict) -> None:
        if get_author(comment) in ADMINS:
            if not self.first_admin_comment:
                self.first_admin_comment = comment

            self.last_admin_comment = comment

            self.add_contact_time(self.created_at,
                                  comment['createdAt'])

            if self.waiting_for_feedback and self.last_community_comment:
                self.add_response_time(self.last_community_comment['createdAt'],
                                       comment['createdAt'])
                self.last_community_comment = None

        else:
            if self.last_admin_comment:
                self.last_community_comment = comment

        self.last_comment = comment

    def get_issue_type(self) -> str:
        for label_name in self.labels.values():
            for issue_type in ISSUE_TYPES:
                if issue_type in label_name.lower():
                    return issue_type

    def get_issue_status(self) -> str:
        for label_name in self.labels.values():
            for issue_status in ISSUE_STATUSES:
                if issue_status in label_name.lower():
                    return issue_status

    def add_contact_time(self, start: str, end: str) -> None:
        # Only add contact time if an admin has commented the issue type has
        # been set or it's closed.
        if self.first_admin_comment and (self.get_issue_type() or self.closed or self.is_pr):
            self.add_metric('time_to_contact', start, end)

    def add_response_time(self, start: str, end: str) -> None:
        if not self.closed:
            self.add_metric('time_to_respond', start, end, multi=True)

    def add_close_time(self, start: str, end: str) -> None:
        self.add_metric(f'time_to_close', start, end)

    def add_metric(self, metric_id: str, start: str, end: str, multi: bool = False) -> None:
        if end > self.end_date:
            return

        if self.is_pr:
            metric_id += '_pr'

        if metric_id not in self.metrics or multi:
            self.metrics[metric_id] = self.metrics.get(metric_id, [])
            self.metrics[metric_id].append(get_delta_days(start, end))


def get_author(element: Dict) -> str:
    author = element['author']

    if author:
        author = author.get('user', author)

    return author.get('login') if author else None


def get_date(element: Dict) -> str:
    if 'createdAt' in element:
        return element['createdAt']
    if 'commit' in element:
        return element['commit']['committedDate']


def get_delta(start: str, end: str) -> timedelta:
    return datetime.strptime(end, DATE_TIME_FORMAT) - datetime.strptime(start, DATE_TIME_FORMAT)


def get_delta_days(start: str, end: str) -> float:
    return get_delta(start, end) / timedelta(days=1)


def get_date_time(date: str) -> str:
    return date + 'T00:00:00Z'


def get_issues(org: str, repo: str, state: str = None,
               start_date: str = '*', end_date: str = '*') -> List[Dict]:
    state = f'state:{state}' if state else ''

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
                '... on PullRequestCommit {commit {committedDate author {user {login}} status {state}}}',
                '... on PullRequestReview {createdAt state author {login}}',
                '... on MergedEvent {createdAt}']
        }
    ]

    inline_fragments = [substitute(fragment_template, fragment)
                        for fragment in fragment_params]

    return post_query(f"""
query{{
    search(type: ISSUE,
           first: 50,
           %cursor%,
           query: "{state} created:{start_date}..{end_date} repo:{org}/{repo}") {{
        nodes {{
            __typename
            {''.join(inline_fragments)}
        }}
        pageInfo {{
            endCursor
            hasNextPage
        }}
    }}
}}""")


def substitute(target: str, values: Dict) -> str:
    for name, value in values.items():
        value = ' '.join(value) if isinstance(value, list) else value
        target = target.replace(f'%{name}%', value)
    return re.sub('%.*?%', '', target)


def post_query(query: str) -> List[Dict]:
    url = 'https://api.github.com/graphql'
    github_token = os.environ['GITHUB_TOKEN']
    headers = {'Authorization': f'token {github_token}'}
    cursor = None

    while True:
        paged_query = substitute(query, {'cursor': f'after: "{cursor}"' if cursor else ''})

        response = requests.post(url, json={'query': paged_query}, headers=headers)
        response.raise_for_status()
        response = response.json()

        if 'data' not in response:
            print_json(response)

        search = response['data']['search']
        for node in search['nodes']:
            yield node

        page_info = search['pageInfo']
        cursor = page_info['endCursor']

        if not page_info['hasNextPage']:
            break


def print_json(payload):
    print(json.dumps(payload, indent=2))


if __name__ == '__main__':
    MetricCollector().run(start_date='2019-01-01',
                          end_date='2019-10-01')
