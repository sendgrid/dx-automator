import types
from datetime import date, datetime, timedelta
from functools import lru_cache
from typing import List

from common.admins import ADMINS
from common.issue import DATE_TIME_FORMAT, get_date, get_issues, Issue, substitute
from common.repos import ALL_REPOS

STUCK_DATE = str(date.today() - timedelta(days=30))
BUG_DATE = str(date.today() - timedelta(days=20))
ENHANCEMENT_DATE = str(date.today() - timedelta(days=60))
TODAY = datetime.utcnow().strftime(DATE_TIME_FORMAT)
TOP_ITEM_COUNT = 10


class ActionItemsCollector:

    def __init__(self):
        self.issues_contact_needed = []
        self.issues_response_needed = []
        self.issues_stuck_waiting = []

        self.prs_contact_needed = []
        self.prs_response_needed = []
        self.prs_stuck_waiting = []

        self.open_bugs = []
        self.open_enhancements = []

    def run(self) -> None:
        for org in ALL_REPOS:
            for repo in ALL_REPOS[org]:
                self.process_repo(org, repo)

        self.print_issues('Issues needing contact', self.issues_contact_needed)
        self.print_issues('Issues needing response', self.issues_response_needed)
        self.print_issues('Issues stuck waiting', self.issues_stuck_waiting)

        self.print_issues('PRs needing contact', self.prs_contact_needed)
        self.print_issues('PRs needing response', self.prs_response_needed)
        self.print_issues('PRs stuck waiting', self.prs_stuck_waiting)

        # Sort aging items by reaction count (desc) and creation date (asc).
        reaction_sort = lambda issue: (-issue.reaction_count, issue.created_at)
        self.print_issues('Aging bugs', self.open_bugs, reaction_sort)
        self.print_issues('Aging enhancements', self.open_enhancements, reaction_sort)

    def print_issues(self, title: str, issues: List[Issue],
                     sort_key=None, reverse_sort=False, divider=None):
        if issues:
            if not sort_key:
                # Default sort by creation date (desc).
                sort_key = lambda issue: issue.created_at
                reverse_sort = True

                # Default split before/after 2020
                divider = lambda issue: issue.created_at >= '2020'

            sorted_top_x = sorted(issues, key=sort_key, reverse=reverse_sort)[:TOP_ITEM_COUNT]

            print(f'\n{title}:')

            if divider:
                top, bottom = [], []
                for x in sorted_top_x:
                    (top if divider(x) else bottom).append(x)

                if top and bottom:
                    print('\n'.join([issue.url for issue in top]))
                    print('-' * 40)
                    print('\n'.join([issue.url for issue in bottom]))
                    return

            print('\n'.join([issue.url for issue in sorted_top_x]))

    def process_repo(self, org: str, repo: str) -> None:
        issues = get_open_items(org, repo)

        for issue_json in issues:
            issue = Issue(issue_json, end_date=TODAY)

            issue.process_events()

            # Required because some merged PRs come back as open.
            # E.g., https://github.com/sendgrid/python-http-client/pull/132
            if issue.merged:
                continue

            if issue.author in ADMINS:
                self.process_pending_issue(issue)
                continue

            if 'time_awaiting_contact' in issue.metrics:
                self.issues_contact_needed.append(issue)
            elif 'time_awaiting_response' in issue.metrics:
                self.issues_response_needed.append(issue)
            elif 'time_awaiting_contact_pr' in issue.metrics:
                self.prs_contact_needed.append(issue)
            elif 'time_awaiting_response_pr' in issue.metrics:
                self.prs_response_needed.append(issue)
            elif issue.waiting_for_feedback:
                if get_date(issue.waiting_for_feedback) < STUCK_DATE and \
                   get_date(issue.last_admin_comment) < STUCK_DATE:
                    if issue.is_pr:
                        self.prs_stuck_waiting.append(issue)
                    else:
                        self.issues_stuck_waiting.append(issue)
            else:
                self.process_pending_issue(issue)

    def process_pending_issue(self, issue: Issue) -> None:
        issue_category = issue.get_issue_category()

        if issue_category == 'bug' and issue.created_at < BUG_DATE:
            self.open_bugs.append(issue)
        elif issue_category == 'twilio_enhancement' and issue.created_at < ENHANCEMENT_DATE:
            self.open_enhancements.append(issue)
        elif issue_category == 'question':
            self.issues_response_needed.append(issue)


@lru_cache(maxsize=None)
def get_open_items(org: str, repo: str):
    fragment_template = """
... on %issue_type% {
    author {
        login
    }
    createdAt
    url
    reactions(content: THUMBS_UP) {
      totalCount
    }
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
                '... on PullRequestCommit {commit {committedDate author {user {login}} status {state} statusCheckRollup {state}}}',
                '... on PullRequestReview {createdAt state author {login}}',
                '... on MergedEvent {createdAt}']
        }
    ]

    inline_fragments = [substitute(fragment_template, fragment)
                        for fragment in fragment_params]

    return list(get_issues(org, repo, ''.join(inline_fragments),
                           issue_state='open'))


if __name__ == '__main__':
    ActionItemsCollector().run()
