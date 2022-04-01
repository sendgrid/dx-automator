from typing import List, Dict

from github import Github, Label as GitHubLabel
from github.Repository import Repository as GitHubRepository

from common.git_hub_api import get_client, submit_graphql_query
from common.labels import Label, get_labels
from common.repos import Repo, get_repos


class GitHubLabelManager:
    def __init__(self, git_hub_client: Github):
        self.client = git_hub_client

    def update_github_labels(self, repos: List[Repo], labels: Dict[str, Label]) -> None:
        error = None

        for repo in repos:
            full_repo_name = f'{repo.org}/{repo.name}'
            print('--------------------------------------------------')
            print('Checking labels: ' + full_repo_name)
            github_repo = self.client.get_repo(full_repo_name, lazy=True)

            try:
                self.update_repo_labels(github_repo, labels)
            except RuntimeError as err:
                error = err

        if error:
            raise error

    def update_repo_labels(self, github_repo: GitHubRepository, labels: Dict[str, Label]) -> None:
        expected_labels = labels.copy()
        labels_with_issues = []

        # Wrap the labels in a list so all pages get pulled. Prevents pagination
        # issues if we delete labels mid-iteration.
        actual_labels = list(github_repo.get_labels())

        for actual_label in actual_labels:
            if actual_label.name in expected_labels:
                self.update_label(actual_label, expected_labels)
            else:
                if not self.delete_label(actual_label, github_repo):
                    labels_with_issues.append(actual_label)

        if labels_with_issues:
            # Don't attempt to create new labels if we have existing labels that we
            # can't delete; they may just need to be renamed.
            raise RuntimeError('found unexpected labels with issues')

        for label in expected_labels.values():
            print('Creating label: ' + label.name)
            github_repo.create_label(label.name, label.color, label.description)

    def update_label(self, actual_label: GitHubLabel, expected_labels: Dict[str, Label]) -> None:
        # Remove the found label from the expected list, so we don't try to
        # create it later.
        expected_label = expected_labels.pop(actual_label.name)

        if not self.are_labels_equal(actual_label, expected_label):
            print('Updating label: ' + actual_label.name)
            actual_label.edit(expected_label.name, expected_label.color, expected_label.description)

    def delete_label(self, actual_label: GitHubLabel, git_hub_repo: GitHubRepository) -> bool:
        # If the label is attached to any issues (or PRs), we don't want to
        # delete it.
        if self.get_label_issue_count(git_hub_repo, actual_label) > 0:
            print('Cannot delete label with issues: ' + actual_label.name)
            return False

        print('Deleting unused label: ' + actual_label.name)
        actual_label.delete()
        return True

    def get_label_issue_count(self, git_hub_repo: GitHubRepository, label: GitHubLabel) -> int:
        response = submit_graphql_query(f"""
query{{
    repository(owner: "{git_hub_repo.organization.login}",
               name: "{git_hub_repo.name}") {{
        label(name: "{label.name}") {{
            issues {{
                totalCount
            }}
            pullRequests {{
                totalCount
            }}
        }}
    }}
}}""")

        response_label = response['repository']['label']

        return (response_label['issues']['totalCount'] +
                response_label['pullRequests']['totalCount'])

    def are_labels_equal(self, actual_label: GitHubLabel, expected_label: Label) -> bool:
        return (actual_label.name == expected_label.name and
                actual_label.color == expected_label.color and
                actual_label.description == expected_label.description)


if __name__ == '__main__':
    manager = GitHubLabelManager(get_client())
    manager.update_github_labels(get_repos(), get_labels())
