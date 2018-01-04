# project/tests/base.py

import json
import unittest

from flask_testing import TestCase

from project import create_app, db

app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()
        self.config()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def config(self):
        return

    def add_with_invalid_json(self, path):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                path,
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
