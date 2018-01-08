import json

from project.tests.base import BaseTestCase

class TestGitHubService(BaseTestCase):
    """Tests for the GitHub Service."""

    def test_is_a_member(self):
        """Ensure the user is a member of your GitHub organization."""
        test_users = [
            'mbernier',
            'thinkingserious',
            'test_exception_user'
        ]
        for user in test_users:
            response = self.client.get(f'/is_a_member/{user}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['is_member'])

        response = self.client.get(f'/is_a_member/fake_user')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['is_member'])

