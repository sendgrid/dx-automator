import json

from project.tests.base import BaseTestCase


class TestGitHubService(BaseTestCase):
    """Tests for the GitHub Service."""

    def test_is_member(self):
        """Ensure the user is a member of your GitHub organization."""
        # TODO: This should be configurable
        test_users = [
            'mitsuhiko',
            'ThiefMaster',
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
            if response.status_code != 200:
                pass # raise AttributeError(user)
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
            'ThiefMaster',
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
        if response.status_code != 200:
            pass # raise AttributeError(len(data))
        self.assertEqual(test_users, data)

        token, self.app.config['GITHUB_TOKEN'] = self.app.config['GITHUB_TOKEN'], 'token'
        response = self.client.get(f'github/members')
        self.assertEqual(response.status_code, 400)
        self.app.config['GITHUB_TOKEN'] = token
