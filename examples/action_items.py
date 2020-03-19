from datetime import date, timedelta
from functools import lru_cache
from typing import List

from examples.common.admins import ADMINS
from examples.common.issue import get_author, get_issues, Issue, substitute
from examples.common.repos import ALL_REPOS

STUCK_DELTA = timedelta(days=30)


class ActionItemsCollector:

    def __init__(self):
        self.contact_needed = []
        self.response_needed = {}
        self.stuck_waiting = {}

        for admin in ADMINS:
            self.response_needed[admin] = []
            self.stuck_waiting[admin] = []

    def run(self, start_date: str) -> None:
        for org in ALL_REPOS:
            for repo in ALL_REPOS[org]:
                self.process_repo(org, repo, start_date)

        self.print_issues('Issues needing contact', self.contact_needed)

        for admin in ADMINS:
            self.print_issues(f'{admin} - Issues needing response', self.response_needed[admin])
            self.print_issues(f'{admin} - Issues stuck waiting', self.stuck_waiting[admin])

    def print_issues(self, title: str, issues: List[Issue]):
        if issues:
            print(f'\n{title}:')
            print('\n'.join([issue.url for issue in issues]))

    def process_repo(self, org: str, repo: str, start_date: str) -> None:
        issues = get_open_items(org, repo, start_date)

        for issue_json in issues:
            issue = Issue(issue_json)

            if issue.author in ADMINS:
                continue

            issue.process_events()

            if 'time_to_contact' not in issue.metrics and 'time_to_contact_pr' not in issue.metrics:
                if issue.is_pr:
                    if issue.checks_passed:
                        self.contact_needed.append(issue)
                else:
                    self.contact_needed.append(issue)

            if issue.is_waiting_for_response:
                self.response_needed[get_author(issue.last_admin_comment)].append(issue)
            elif issue.waiting_for_feedback and \
                issue.waiting_for_feedback['createdAt'] < str(date.today() - STUCK_DELTA):
                self.stuck_waiting[get_author(issue.last_admin_comment)].append(issue)


@lru_cache(maxsize=None)
def get_open_items(org: str, repo: str, start_date: str):
    fragment_template = """
... on %issue_type% {
    author {
        login
    }
    createdAt
    url
    timelineItems(first: 100, itemTypes: [LABELED_EVENT UNLABELED_EVENT ISSUE_COMMENT
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
            'additional_event_names': ['PULL_REQUEST_COMMIT', 'PULL_REQUEST_REVIEW'],
            'additional_event_types': [
                '... on PullRequestCommit {commit {committedDate author {user {login}} status {state}}}',
                '... on PullRequestReview {createdAt state author {login}}']
        }
    ]

    inline_fragments = [substitute(fragment_template, fragment)
                        for fragment in fragment_params]

    return list(get_issues(org, repo, ''.join(inline_fragments),
                           state='open', start_date=start_date))


if __name__ == '__main__':
    ActionItemsCollector().run(start_date='2019-11-01')
