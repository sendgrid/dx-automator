import os
import unittest
from collections import namedtuple
from unittest.mock import patch, Mock

from common.repos import Repo
from examples.update_git_hub_labels import GitHubLabelManager


@patch.dict(os.environ, {"GITHUB_TOKEN": "THE TOKEN"})
class TestGitHubLabelManager(unittest.TestCase):
    def setUp(self):
        self.label = Mock()
        self.label.name = 'label name'
        self.label.color = 'label color'
        self.label.description = 'label desc'
        self.label.edit = Mock()
        self.label.delete = Mock()

        self.expected_label = Mock()
        self.expected_label.name = 'label name'
        self.expected_label.color = 'updated color'
        self.expected_label.description = 'updated desc'

        self.new_label = Mock()
        self.new_label.name = 'new label'
        self.new_label.color = 'new color'
        self.new_label.description = 'new desc'

        self.git_hub_repo = Mock()
        self.git_hub_repo.organization = Mock()
        self.git_hub_repo.organization.login = 'twilio'
        self.git_hub_repo.name = 'twilio-node'
        self.git_hub_repo.get_labels.return_value = [self.label]

        self.git_hub_client_mock = Mock()
        self.git_hub_client_mock.get_repo.return_value = self.git_hub_repo

        self.manager = GitHubLabelManager(self.git_hub_client_mock)

    def test_update_github_labels(self):
        repos = [
            Repo('twilio', 'twilio-node'),
        ]
        labels = {
            self.expected_label.name: self.expected_label,
            self.new_label.name: self.new_label,
        }

        self.manager.update_github_labels(repos, labels)

        self.label.edit.assert_called_once_with('label name', 'updated color', 'updated desc')
        self.git_hub_repo.create_label.assert_called_once_with('new label', 'new color', 'new desc')

    @patch('examples.update_git_hub_labels.submit_graphql_query')
    def test_update_github_labels_with_issues(self, graphql_mock):
        graphql_mock.return_value = {
            'repository': {
                'label': {
                    'issues': {
                        'totalCount': 1
                    },
                    'pullRequests': {
                        'totalCount': 0
                    },
                },
            },
        }

        repos = [
            Repo('twilio', 'twilio-node'),
        ]
        labels = {}

        self.assertRaises(RuntimeError, self.manager.update_github_labels, repos, labels)

        self.label.edit.assert_not_called()
        self.label.delete.assert_not_called()
        self.git_hub_repo.create_label.assert_not_called()

    def test_update_label(self):
        expected_labels = {
            self.expected_label.name: self.expected_label
        }

        self.manager.update_label(self.label, expected_labels)
        self.label.edit.assert_called_once_with('label name', 'updated color', 'updated desc')

    def test_update_label_match(self):
        expected_labels = {
            self.label.name: self.label
        }

        self.manager.update_label(self.label, expected_labels)
        self.label.edit.assert_not_called()

    @patch('examples.update_git_hub_labels.submit_graphql_query')
    def test_delete_label(self, graphql_mock):
        graphql_mock.return_value = {
            'repository': {
                'label': {
                    'issues': {
                        'totalCount': 0
                    },
                    'pullRequests': {
                        'totalCount': 0
                    },
                },
            },
        }

        self.assertTrue(self.manager.delete_label(self.label, self.git_hub_repo))
        self.label.delete.assert_called_once()

    @patch('examples.update_git_hub_labels.submit_graphql_query')
    def test_delete_label_with_issues(self, graphql_mock):
        graphql_mock.return_value = {
            'repository': {
                'label': {
                    'issues': {
                        'totalCount': 0
                    },
                    'pullRequests': {
                        'totalCount': 100
                    },
                },
            },
        }

        self.assertFalse(self.manager.delete_label(self.label, self.git_hub_repo))
        self.label.delete.assert_not_called()

    def test_are_labels_equal(self):
        label_type = namedtuple('Label', 'name color description')

        actual_label = label_type('name', 'color', 'desc')
        expected_label = label_type('name', 'color', 'desc')
        self.assertTrue(self.manager.are_labels_equal(actual_label, expected_label))

        expected_label = label_type('name', 'color', 'different')
        self.assertFalse(self.manager.are_labels_equal(actual_label, expected_label))

        expected_label = label_type('name', 'different', 'desc')
        self.assertFalse(self.manager.are_labels_equal(actual_label, expected_label))

        expected_label = label_type('different', 'color', 'desc')
        self.assertFalse(self.manager.are_labels_equal(actual_label, expected_label))
