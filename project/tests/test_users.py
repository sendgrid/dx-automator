# project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User

def add_user(github_username, email_address, twitter_username):
    user = User(github_username=github_username,
                email_address=email_address,
                twitter_username=twitter_username)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def config(self):
        pass

    def test_base_route(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping_user')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            github_username = 'thinkingserious'
            email_address = 'elmer.thomas@sendgrid.com'
            twitter_username = 'thinkingserious'
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    github_username=github_username,
                    email_address=email_address,
                    twitter_username=twitter_username
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('{0} was added!'.format(github_username), data['message'])
            self.assertIn('success', data['status'])
