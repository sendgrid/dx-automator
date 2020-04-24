from functools import lru_cache

from common.admins import ADMINS
from common.issue import get_date_time, get_issues, Issue
from common.repos import ALL_REPOS


class ClosedItemsCollector:

    def __init__(self):
        self.community_issues = 0
        self.community_prs = 0
        self.admin_issues = 0
        self.admin_prs = 0

    def run(self, start_date: str, end_date: str) -> None:
        for org in ALL_REPOS:
            for repo in ALL_REPOS[org]:
                self.process_repo(org, repo, start_date, end_date)

        print(f'Closed community issues: {self.community_issues}')
        print(f'Merged community PRs: {self.community_prs}')
        print(f'Closed admin issues: {self.admin_issues}')
        print(f'Merged admin PRs: {self.admin_prs}')

    def process_repo(self, org: str, repo: str,
                     start_date: str, end_date: str) -> None:
        start_date = get_date_time(start_date)
        end_date = get_date_time(end_date)

        issues = get_closed_items(org, repo)

        for issue_json in issues:
            issue = Issue(issue_json, end_date=end_date)
            issue.process_events()

            close_event = issue.merged if issue.is_pr else issue.closed

            if close_event and start_date <= close_event['createdAt'] < end_date:
                if issue.author in ADMINS:
                    if issue.is_pr:
                        self.admin_prs = self.admin_prs + 1
                    else:
                        self.admin_issues = self.admin_issues + 1
                else:
                    if issue.is_pr:
                        self.community_prs = self.community_prs + 1
                    else:
                        self.community_issues = self.community_issues + 1


@lru_cache(maxsize=None)
def get_closed_items(org: str, repo: str):
    fragments = """
... on Issue {
    author {
        login
    }
    createdAt
    url
    timelineItems(first: 100, itemTypes: [CLOSED_EVENT]) {
        nodes {
            __typename
            ... on ClosedEvent {
                createdAt
            }
        }
    }
}
... on PullRequest {
    author {
        login
    }
    createdAt
    url
    timelineItems(first: 100, itemTypes: [MERGED_EVENT]) {
        nodes {
            __typename
            ... on MergedEvent {
                createdAt
            }
        }
    }
}"""

    return list(get_issues(org, repo, fragments, issue_state='closed'))


if __name__ == '__main__':
    ClosedItemsCollector().run(start_date='2019-10-01',
                               end_date='2020-01-01')
    ClosedItemsCollector().run(start_date='2020-01-01',
                               end_date='2020-04-01')
