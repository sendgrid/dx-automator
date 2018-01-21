# project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Item, ItemStatus

url_issue_1 = 'https://github.com/SendGridDX/testing-playground/issues/1'
url_issue_2 = 'https://github.com/SendGridDX/testing-playground/issues/2'


def add_item(subject, url, requestor):
    item = Item(subject=subject, url=url, requestor=requestor)
    db.session.add(item)
    db.session.commit()
    return item


class TestItemService(BaseTestCase):
    """Tests for the Items Service."""

    def config(self):
        """Make sure the foreign key is there!"""
        db.session.add(
        ItemStatus(
            name="Intake",
            value="1000000000",
            value_type="multiplier"
            ))
        db.session.commit()

    def test_base_route(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_item(self):
        """Ensure a new item can be added to the database."""
        with self.client:
            subject = 'A test item to be added'
            url = url_issue_1
            response = self.client.post(
                '/items',
                data=json.dumps(dict(
                    subject=subject,
                    url=url,
                    requestor='a_github_user'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('{0} was added!'.format(subject), data['message'])
            self.assertIn('success', data['status'])

    def test_add_item_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        self.add_with_invalid_json('/items')

    def test_add_item_missing_url_json_keys(self):
        """Ensure error is thrown if the JSON
        object does not have a url key."""
        with self.client:
            response = self.client.post(
                '/items',
                data=json.dumps(dict(
                    subject='This is a test subject',
                    url=url_issue_1
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_item_missing_requestor_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a requestor key."""
        with self.client:
            url = url_issue_1
            response = self.client.post(
                '/items',
                data=json.dumps(dict(
                    subject='This is a test subject',
                    url=url
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_item_missing_subject_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a subject key."""
        with self.client:
            url = url_issue_1
            response = self.client.post(
                '/items',
                data=json.dumps(dict(
                    url=url,
                    requestor='foo'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_item_duplicate_item(self):
        """Ensure error is thrown if the item already exists."""
        with self.client:
            subject = 'A test item to be added'
            self.client.post(
                '/items',
                data=json.dumps(dict(
                    subject=subject,
                    url=url_issue_1,
                    requestor='a_github_user'
                )),
                content_type='application/json',
            )
            response = self.client.post(
                '/items',
                data=json.dumps(dict(
                    subject=subject,
                    url=url_issue_1,
                    requestor='a_github_user'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'item already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_item(self):
        """Ensure get single item behaves correctly."""
        item = add_item('A test item to be added',
                        url_issue_1,
                        'a_github_user')
        with self.client:
            response = self.client.get('/items/{0}'.format(item.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertTrue('updated_at' in data['data'])
            self.assertIn('A test item to be added', data['data']['subject'])
            self.assertIn(
                url_issue_1, data['data']['url'])
            self.assertIn('a_github_user', data['data']['requestor'])
            self.assertIn('success', data['status'])

    def test_single_item_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/items/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Item does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_item_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/items/0')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Item does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_items(self):
        """Ensure get all items behaves correctly."""
        add_item('A test item to be added',
                 url_issue_1,
                 'a_github_user')
        add_item('Another test item to be added',
                 url_issue_2,
                 'a_2nd_github_user')
        with self.client:
            response = self.client.get('/items')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['items']), 2)
            # First Item
            self.assertTrue('created_at' in data['data']['items'][0])
            self.assertTrue('updated_at' in data['data']['items'][0])
            self.assertTrue('due_date' in data['data']['items'][0])
            self.assertIn('A test item to be added',
                          data['data']['items'][0]['subject'])
            self.assertIn(url_issue_1,
                          data['data']['items'][0]['url'])
            self.assertIn('a_github_user',
                          data['data']['items'][0]['requestor'])
            self.assertTrue('maintainer' in data['data']['items'][0])
            # Second Item
            self.assertTrue('created_at' in data['data']['items'][1])
            self.assertTrue('updated_at' in data['data']['items'][1])
            self.assertTrue('due_date' in data['data']['items'][1])
            self.assertIn('Another test item to be added',
                          data['data']['items'][1]['subject'])
            self.assertIn(url_issue_2,
                          data['data']['items'][1]['url'])
            self.assertIn('a_2nd_github_user',
                          data['data']['items'][1]['requestor'])
            self.assertTrue('maintainer' in data['data']['items'][1])

            self.assertIn('success', data['status'])


    def test_edit_item(self):
        """Ensure we can edit an item."""
        with self.client:
            subject = 'A editable item'
            url = url_issue_1
            response = self.client.post(
                '/items',
                data=json.dumps(dict(
                    subject=subject,
                    url=url,
                    requestor='a_github_user'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('{0} was added!'.format(subject), data['message'])
            self.assertIn('success', data['status'])

            # Attempt to edit the subject and url
            subject = 'A edited item'
            url = url_issue_2
            github_username = 'a_github_user'
            response = self.client.patch(
                '/items/{0}'.format(data['data']['id']),
                data=json.dumps(dict(
                    subject=subject,
                    url=url,
                    requestor=github_username
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(subject, data['data']['subject'])
            self.assertIn(url_issue_2, data['data']['url'])
            self.assertIn(github_username, data['data']['requestor'])

            # Verify the data was stored correctly
            response = self.client.get('/items/{0}'.format(data['data']['id']))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(subject, data['data']['subject'])
            self.assertIn(url_issue_2, data['data']['url'])
            self.assertIn('success', data['status'])

    def test_items_equal(self):
        """Ensure we can detect two equal and unequal items."""
        item_1 = add_item('A test item to be added',
                    url_issue_1,
                    'a_github_user')
        item_2 = add_item('Another test item to be added',
                    url_issue_2,
                    'a_2nd_github_user')
        self.assertEqual(False, Item.items_equal(item_1, item_2))
        item_3 = add_item('A test item to be added',
                    url_issue_1,
                    'a_github_user')
        self.assertEqual(True, Item.items_equal(item_1, item_3))