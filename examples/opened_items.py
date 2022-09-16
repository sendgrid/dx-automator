from common.admins import ADMINS
from common.issue import get_issues, Issue
from common.repos import ALL_REPOS


class OpenedItemsCollector:

    def __init__(self):
        self.community_issues = 0
        self.community_prs = 0
        self.admin_issues = 0
        self.admin_prs = 0

    def run(self, start_date: str, end_date: str) -> None:
        for org in ALL_REPOS:
            for repo in ALL_REPOS[org]:
                self.process_repo(org, repo, start_date, end_date)

        print(f'Opened community issues: {self.community_issues}')
        print(f'Opened community PRs: {self.community_prs}')
        print(f'Opened admin issues: {self.admin_issues}')
        print(f'Opened admin PRs: {self.admin_prs}')

    def process_repo(self, org: str, repo: str,
                     start_date: str, end_date: str) -> None:
        issues = get_opened_items(org, repo, start_date, end_date)

        for issue_json in issues:
            issue = Issue(issue_json, end_date=end_date)

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


def get_opened_items(org: str, repo: str, start_date: str, end_date: str):
    fragments = """
... on Issue {
    author {
        login
    }
    createdAt
    closedAt
    url
}
... on PullRequest {
    author {
        login
    }
    createdAt
    url
}"""

    return list(get_issues(org, repo, fragments, start_date=start_date, end_date=end_date))


if __name__ == '__main__':
    OpenedItemsCollector().run(start_date='2019-07-01',
                               end_date='2019-10-01')
    OpenedItemsCollector().run(start_date='2019-10-01',
                               end_date='2020-01-01')
