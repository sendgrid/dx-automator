import unittest

from examples.common.repos import ALL_REPOS, get_repos, is_repo_included


class TestRepos(unittest.TestCase):

    def test_is_repo_included(self):
        self.assertTrue(is_repo_included('twilio', 'twilio-cli', [], [], []))
        self.assertTrue(is_repo_included('twilio', 'twilio-cli', ['twilio'], [], []))
        self.assertTrue(is_repo_included('twilio', 'twilio-cli', [], ['twilio-cli'], []))
        self.assertTrue(is_repo_included('twilio', 'twilio-cli', [], [], ['twilio-csharp']))
        self.assertTrue(is_repo_included('twilio', 'twilio-cli', ['sendgrid'], ['twilio-cli'], []))

        self.assertFalse(is_repo_included('twilio', 'twilio-cli', ['sendgrid'], [], []))
        self.assertFalse(is_repo_included('twilio', 'twilio-cli', [], ['twilio-csharp'], []))
        self.assertFalse(is_repo_included('twilio', 'twilio-cli', [], [], ['twilio-cli']))

    def test_get_repos(self):
        total_repos_length = len([repo for org in ALL_REPOS for repo in ALL_REPOS[org]])
        self.assertEqual(total_repos_length, len(get_repos()))

        self.assertEqual(1, len(get_repos(include_repos=['twilio-node'])))
        self.assertTrue(all(repo.org == 'sendgrid' for repo in get_repos(include_orgs=['sendgrid'])))
