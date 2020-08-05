import json

from project.tests.base import BaseTestCase


class TestGitHubService(BaseTestCase):
    """Tests for the GitHub Service."""

    def test_health_check(self):
        response = self.client.get('github/ping')
        self.assertEqual(response.status_code, 200)

    def test_is_member(self):
        """Ensure the user is a member of your GitHub organization."""
        # TODO: This should be configurable
        test_users = [
            'mitsuhiko',
            'Thief,
            'lepture',
            'jeffwidman',
            'untitaker',
            'edk0',
            'davidism',
            'pgjones',
            'miguelgrinberg',
            'dawran6',
            'keyan',
            'greyli',
            'jcrotts',
            'test_exception_user'
        ]
        for user in test_users:
            response = self.client.get(f'github/is_member/{user}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertTrue(data['is_member'])

        response = self.client.get(f'github/is_member/octocat')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['is_member'])

        token, self.app.config['GITHUB_TOKEN'] = self.app.config['GITHUB_TOKEN'], 'token'
        response = self.client.get(f'github/is_member/octocat')
        self.assertEqual(response.status_code, 400)
        self.app.config['GITHUB_TOKEN'] = token

    def test_get_all_members(self):
        """Ensure all the users are a member of your GitHub organization."""
        # TODO: This should be configurable
        test_users = [
            'mitsuhiko',
            'Thief',
            'lepture',
            'jeffwidman',
            'untitaker',
            'edk0',
            'davidism',
            'pgjones',
            'miguelgrinberg',
            'dawran6',
            'keyan',
            'greyli',
            'jcrotts'
        ]
        response = self.client.get(f'github/members')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(test_users, data)

        token, self.app.config['GITHUB_TOKEN'] = self.app.config['GITHUB_TOKEN'], 'token'
        response = self.client.get(f'github/members')
        self.assertEqual(response.status_code, 400)
        self.app.config['GITHUB_TOKEN'] = token

    def test_get_all_open_prs(self):
        """Get all the PRs for the chosen github repo."""
        test_repo = 'sendgrid-python'
        response = self.client.get(f'github/open_pr_urls/{test_repo}')
        self.assertEqual(response.status_code, 200)
