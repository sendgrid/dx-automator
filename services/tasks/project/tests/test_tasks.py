# services/tasks/project/tests/test_tasks.py


import json
import unittest

from project import db
from project.api.models import Task
from project.tests.base import BaseTestCase


def add_task(creator, url):
    task = Task(creator=creator, url=url)
    db.session.add(task)
    db.session.commit()
    return task


class TestTaskService(BaseTestCase):
    """Tests for the Tasks Service."""

    def test_tasks(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/tasks/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_single_task(self):
        """Ensure a new task can be added to the database."""
        with self.client:
            response = self.client.post(
                '/tasks',
                data=json.dumps({
                    'creator': 'anshul',
                    'url': 'anshulsinghal.me'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('anshulsinghal.me was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_task_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/tasks',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a taskname key.
        """
        with self.client:
            response = self.client.post(
                '/tasks',
                data=json.dumps({'phone': '999999999'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    # def test_add_task_duplicate_link(self):
    #     """Ensure error is thrown if the email already exists."""
    #     with self.client:
    #         self.client.post(
    #             '/tasks',
    #             data=json.dumps({
    #                 'creator': 'anshul',
    #                 'link': 'anshulsinghal.me'
    #             }),
    #             content_type='application/json',
    #         )
    #         response = self.client.post(
    #             '/tasks',
    #             data=json.dumps({
    #                 'creator': 'anshul',
    #                 'link': 'anshulsinghal.me'
    #             }),
    #             content_type='application/json',
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(response.status_code, 400)
    #         self.assertIn(
    #             'Sorry. That link already exists.', data['message'])
    #         self.assertIn('fail', data['status'])

    def test_single_task(self):
        """Ensure get single task behaves correctly."""
        task = add_task(creator='anshul', url='anshulsinghal.me')
        with self.client:
            response = self.client.get(f'/tasks/{task.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('anshul', data['data']['creator'])
            self.assertIn('anshulsinghal.me', data['data']['url'])
            self.assertIn('success', data['status'])

    def test_single_task_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/tasks/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('task does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_tasks(self):
        """Ensure get all tasks behaves correctly."""
        add_task('anshul', 'anshulsinghal.me')
        add_task('another', 'another.com')
        with self.client:
            response = self.client.get('/tasks')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['tasks']), 2)
            self.assertIn('anshul', data['data']['tasks'][0]['creator'])
            self.assertIn(
                'anshulsinghal.me', data['data']['tasks'][0]['url'])
            self.assertIn('another', data['data']['tasks'][1]['creator'])
            self.assertIn(
                'another.com', data['data']['tasks'][1]['url'])
            self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()
