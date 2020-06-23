from datetime import date, datetime, timedelta
from functools import lru_cache
from typing import List

from common.admins import ADMINS
from common.issue import DATE_TIME_FORMAT, get_author, get_date, get_issues, Issue, substitute
from common.repos import ALL_REPOS

STUCK_DATE = str(date.today() - timedelta(days=30))
BUG_DATE = str(date.today() - timedelta(days=20))
ENHANCEMENT_DATE = str(date.today() - timedelta(days=60))
TODAY = datetime.utcnow().strftime(DATE_TIME_FORMAT)


class ActionItemsCollector:

    def __init__(self):
        self.contact_needed = []
        self.response_needed = {}
        self.stuck_waiting = {}
        self.open_bugs = []
        self.open_enhancements = []

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

        self.print_issues('Aging bugs', self.open_bugs)
        self.print_issues('Aging enhancements', self.open_enhancements)

    def print_issues(self, title: str, issues: List[Issue]):
        if issues:
            sorted_issues = sorted(issues, key=lambda issue: (not issue.is_pr, issue.created_at))

            print(f'\n{title}:')
            print('\n'.join([issue.url for issue in sorted_issues]))

    def process_repo(self, org: str, repo: str, start_date: str) -> None:
        issues = get_open_items(org, repo, start_date)

        for issue_json in issues:
            issue = Issue(issue_json, end_date=TODAY)

            issue.process_events()

            # Required because some merged PRs come back as open.
            # E.g., https://github.com/sendgrid/python-http-client/pull/132
            if issue.merged:
                continue

            if 'time_awaiting_contact' in issue.metrics or \
               'time_awaiting_contact_pr' in issue.metrics:
                self.contact_needed.append(issue)
            elif 'time_awaiting_response' in issue.metrics or \
                 'time_awaiting_response_pr' in issue.metrics:
                self.response_needed[get_author(issue.last_admin_comment)].append(issue)
            elif issue.waiting_for_feedback:
                if get_date(issue.waiting_for_feedback) < STUCK_DATE and \
                   get_date(issue.last_admin_comment) < STUCK_DATE:
                    self.stuck_waiting[get_author(issue.last_admin_comment)].append(issue)
            else:
                if issue.get_issue_category() == 'bug':
                    if issue.created_at < BUG_DATE:
                        self.open_bugs.append(issue)
                else:
                    if issue.created_at < ENHANCEMENT_DATE:
                        self.open_enhancements.append(issue)


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

    return list(get_issues(org, repo, ''.join(inline_fragments),
                           issue_state='open', start_date=start_date))


if __name__ == '__main__':
    ActionItemsCollector().run(start_date='2019-07-01')
