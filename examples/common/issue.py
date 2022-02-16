import json
from datetime import datetime, timedelta
from typing import Dict, Iterator

from businesstime import BusinessTime
from businesstime.holidays.usa import USFederalHolidays

from common.admins import ADMINS
from common.git_hub_api import submit_graphql_query

ISSUE_CATEGORIES = {
    'question': {'question', 'getting started'},
    'support': {'support', 'non-library'},
    'bug': {'bug', 'docs', 'security'},
    'twilio_enhancement': {'twilio enhancement', 'sendgrid enhancement'},
    'community_enhancement': {'community enhancement'},
}
ISSUE_STATUSES = {'duplicate', 'invalid'}

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

BUSINESS_TIME = BusinessTime(holidays=USFederalHolidays())


class Issue:
    def __init__(self, issue_json: Dict, end_date: str):
        try:
            self.issue_json = issue_json
            self.end_date = end_date
            self.author = get_author(issue_json)
            self.type = issue_json['__typename']
            self.created_at = issue_json['createdAt']
            self.url = issue_json['url']
            self.reaction_count = issue_json.get('reactions', {}).get('totalCount')

            if 'timelineItems' in issue_json:
                self.events = issue_json['timelineItems']['nodes']

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

                if event_type in ['LabeledEvent', 'UnlabeledEvent'] or \
                    not self.is_past_end_date(event):
                    action = event_type_map[event_type]
                    action(event)

            if not self.closed and not self.merged:
                if 'time_to_contact' not in self.metrics and 'time_to_contact_pr' not in self.metrics:
                    if self.is_pr:
                        if self.checks_passed:
                            self.add_awaiting_time('contact', self.checks_passed)
                    else:
                        self.add_awaiting_time('contact', self.created_at)
                elif self.is_waiting_for_response:
                    self.add_awaiting_time('response', self.last_community_comment)
                elif not self.waiting_for_feedback:
                    self.add_awaiting_time('resolution', self.last_event)
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

        if self.is_past_end_date(label_event):
            return

        self.add_contact_time(self.created_at, label_event)

        if 'waiting' in label['name'].lower():
            self.waiting_for_feedback = label_event

        if 'type:' in label['name'].lower():
            self.type_added = label_event

    def remove_label(self, label_event: Dict) -> None:
        label = label_event['label']

        # Safely remove label.
        self.labels.pop(label['id'], None)

        if self.is_past_end_date(label_event):
            return

        if 'waiting' in label['name'].lower():
            self.waiting_removed = label_event

            if self.is_waiting_for_response:
                self.add_response_time(self.last_community_comment, label_event)
            self.waiting_for_feedback = None

    def close(self, close_event: Dict) -> None:
        self.closed = close_event

        self.add_close_time(self.last_event, close_event)

        # If there's no contact time yet, use the first admin comment.
        if self.first_admin_comment:
            self.add_contact_time(self.created_at, self.first_admin_comment)

    def reopen(self, reopen_event: Dict) -> None:
        self.closed = None

    def commit(self, commit_event: Dict) -> None:
        commit = commit_event['commit']

        # status is sometimes null so fallback to the rollup if needed.
        # https://github.community/t/graphql-api-response-for-commit-status-is-null/
        status = commit['status'] or commit['statusCheckRollup'] or {}
        self.checks_passed = commit if status.get('state') == 'SUCCESS' else None

        # Treat this as a comment if from non-admin and the checks passed.
        if get_author(commit) not in ADMINS and self.checks_passed:
            self.comment(commit)

    def review(self, review_event: Dict) -> None:
        if get_author(review_event) in ADMINS:
            self.comment(review_event)
            self.waiting_for_feedback = None if review_event['state'] == 'APPROVED' else review_event

    def merge(self, merge_event: Dict) -> None:
        self.merged = merge_event

    def comment(self, comment: Dict) -> None:
        if get_author(comment) in ADMINS:
            if not self.first_admin_comment:
                self.first_admin_comment = comment

            self.last_admin_comment = comment

            self.add_contact_time(self.created_at, comment)

            if self.is_waiting_for_response:
                self.add_response_time(self.last_community_comment, comment)

            # Clear the community comment since it's no longer needed. Either
            # we were waiting for a response and it was clocked or we weren't
            # and just commented on the issue anyway.
            self.last_community_comment = None

            if self.is_pr:
                # Treat admin PR comments like unapproved review events.
                self.waiting_for_feedback = comment

        else:
            if self.last_admin_comment:
                self.last_community_comment = comment

        self.last_comment = comment

    def get_issue_category(self) -> str:
        for label_name in self.labels.values():
            for issue_category, issues_types in ISSUE_CATEGORIES.items():
                for issue_type in issues_types:
                    if issue_type in label_name.lower():
                        return issue_category

    def get_issue_status(self) -> str:
        for label_name in self.labels.values():
            for issue_status in ISSUE_STATUSES:
                if issue_status in label_name.lower():
                    return issue_status

    def add_contact_time(self, start, end) -> None:
        # Only add contact time if an admin has commented the issue type has
        # been set or it's closed.
        if self.first_admin_comment and (self.get_issue_category() or self.closed or self.is_pr):
            self.add_metric('time_to_contact', start, end)

    def add_response_time(self, start, end) -> None:
        if not self.closed:
            self.add_metric('time_to_respond', start, end, multi=True)

    def add_close_time(self, start, end) -> None:
        self.add_metric('time_to_close', start, end)

    def add_awaiting_time(self, action: str, start) -> None:
        self.add_metric(f'time_awaiting_{action}', start, self.end_date)

    def add_metric(self, metric_id: str, start, end, multi: bool = False) -> None:
        start = get_date(start)
        end = get_date(end)

        if self.is_pr:
            metric_id += '_pr'

        if metric_id not in self.metrics or multi:
            self.metrics[metric_id] = self.metrics.get(metric_id, [])
            self.metrics[metric_id].append(get_delta_days(start, end))

    @property
    def last_event(self):
        if self.waiting_removed:
            return self.waiting_removed

        if self.type_added:
            return self.type_added

        if self.checks_passed:
            return self.checks_passed

        return self.created_at

    def is_past_end_date(self, element):
        return self.end_date and get_date(element) > self.end_date


def get_author(element: Dict) -> str:
    author = element['author']

    if author:
        author = author.get('user', author)

    return author.get('login') if author else None


def get_date(element) -> str:
    if isinstance(element, dict):
        if 'createdAt' in element:
            return element['createdAt']
        if 'committedDate' in element:
            return element['committedDate']
        if 'commit' in element:
            return element['commit']['committedDate']

    return element


def get_delta_days(start: str, end: str) -> float:
    return get_delta(start, end) / timedelta(days=1)


def get_delta(start: str, end: str) -> timedelta:
    return BUSINESS_TIME.businesstimedelta(datetime.strptime(start, DATE_TIME_FORMAT),
                                           datetime.strptime(end, DATE_TIME_FORMAT))


def get_date_time(date: str) -> str:
    return date + 'T00:00:00Z'


def get_issues(org: str, repo: str, fragments: str,
               issue_type: str = None, issue_state: str = None,
               start_date: str = '*', end_date: str = '*') -> Iterator[Dict]:
    issue_type = f'type:{issue_type}' if issue_type else ''
    issue_state = f'state:{issue_state}' if issue_state else ''

    return submit_graphql_query(f"""
query{{
    search(type: ISSUE,
           first: 50,
           %cursor%,
           query: "{issue_type} {issue_state} created:{start_date}..{end_date} repo:{org}/{repo}") {{
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


def print_json(payload):
    print(json.dumps(payload, indent=2))
