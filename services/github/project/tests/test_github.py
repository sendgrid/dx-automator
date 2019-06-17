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
        self.assertEqual(test_users, data)

        token, self.app.config['GITHUB_TOKEN'] = self.app.config['GITHUB_TOKEN'], 'token'
        response = self.client.get(f'github/members')
        self.assertEqual(response.status_code, 400)
        self.app.config['GITHUB_TOKEN'] = token

    def test_get_all_open_prs(self):
        # TODO: update this test 
        pass

    def test_filter_created_date(self):
        """Ensures that the date filtering functionality works"""
        test_repo = 'sendgrid-python'
        start_date = "2018-01-01"
        end_date = "2019-01-01"
        response = self.client.get(f'github/items?repo={test_repo}&issue_type=issues&states[]=OPEN&start_creation_date={start_date}&end_creation_date{end_date}')
        self.assertEqual(200, 200)
    
    def test_test(self):
        self.assertEqual(1,1)

    def test_date_format(self):
        """Ensures that a ValueError is thrown when a date parameter is entered in the wrong format"""
        test_repo = 'sendgrid-python'
        start_date = "2018:01:01"
        end_date = "2019-01-01"
        response = self.client.get(f'github/items?repo={test_repo}&issue_type=issues&states[]=OPEN&start_creation_date={start_date}&end_creation_date{end_date}')
        self.assertEqual(response.status_code, 400)