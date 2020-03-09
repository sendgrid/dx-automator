import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List

import requests
from businesstime import BusinessTime
from businesstime.holidays.usa import USFederalHolidays

from examples.common.admins import ADMINS

ISSUE_TYPES = {'question', 'support', 'bug', 'enhancement', 'non-library', 'docs', 'security'}
ISSUE_STATUSES = {'duplicate', 'invalid'}

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

BUSINESS_TIME = BusinessTime(holidays=USFederalHolidays())


class Issue:
    def __init__(self, issue_json: Dict, end_date: str = None):
        try:
            self.issue_json = issue_json
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
        except Exception as e:
            print_json(self.issue_json)
            raise e

    def process_events(self):
        event_type_map = {
            'LabeledEvent': self.add_label,
            'UnlabeledEvent': self.remove_label,
            'IssueComment': self.comment,
            'ClosedEvent': self.close,
            'ReopenedEvent': self.reopen,
            'PullRequestCommit': self.commit,
            'PullRequestReview': self.review,
            'MergedEvent': self.merge,
        }

        try:
            for event in self.events:
                event_type = event['__typename']
                action = event_type_map[event_type]
                action(event)
        except Exception as e:
            print_json(self.issue_json)
            raise e

    @property
    def is_pr(self):
        return self.type == 'PullRequest'

    @property
    def is_waiting_for_response(self):
        return self.waiting_for_feedback and self.last_community_comment

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

            if self.is_waiting_for_response:
                self.add_response_time(self.last_community_comment['createdAt'],
                                       label_event['createdAt'])
            self.waiting_for_feedback = None

    def close(self, close_event: Dict) -> None:
        if self.end_date and close_event['createdAt'] > self.end_date:
            return

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
        if self.end_date and reopen_event['createdAt'] > self.end_date:
            return

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

            if self.is_waiting_for_response:
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
        if self.end_date and end > self.end_date:
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


def get_delta_days(start: str, end: str) -> float:
    return get_delta(start, end) / timedelta(days=1)


def get_delta(start: str, end: str) -> timedelta:
    return BUSINESS_TIME.businesstimedelta(datetime.strptime(start, DATE_TIME_FORMAT),
                                           datetime.strptime(end, DATE_TIME_FORMAT))


def get_date_time(date: str) -> str:
    return date + 'T00:00:00Z'


def get_issues(org: str, repo: str, fragments: str,
               type: str = None, state: str = None,
               start_date: str = '*', end_date: str = '*') -> List[Dict]:
    type = f'type:{type}' if type else ''
    state = f'state:{state}' if state else ''

    return post_query(f"""
query{{
    search(type: ISSUE,
           first: 50,
           %cursor%,
           query: "{type} {state} created:{start_date}..{end_date} repo:{org}/{repo}") {{
        nodes {{
            __typename
            {fragments}
        }}
        pageInfo {{
            endCursor
            hasNextPage
        }}
    }}
}}""")


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


def substitute(target: str, values: Dict) -> str:
    for name, value in values.items():
        value = ' '.join(value) if isinstance(value, list) else value
        target = target.replace(f'%{name}%', value)
    return re.sub('%.*?%', '', target)


def print_json(payload):
    print(json.dumps(payload, indent=2))
