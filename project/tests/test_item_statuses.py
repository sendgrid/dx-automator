# project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import ItemStatus

status_1 = 'status_1'
status_2 = 'status_2'

def add_item_status(name, value, value_type):
    item_status = ItemStatus(name=name, value=value, value_type=value_type)
    db.session.add(item_status)
    db.session.commit()
    return item_status


class TestItemStatusService(BaseTestCase):
    """Tests for the Item Status Service."""

    def test_add_item_status(self):
        """Ensure a new item can be added to the database."""
        with self.client:
            name = status_1
            value = 1
            value_type = 'Multiplier'

            response = self.client.post(
                '/item_statuses',
                data=json.dumps(dict(
                    name=name,
                    value=value,
                    value_type=value_type
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('{0} was added!'.format(name), data['message'])
            self.assertIn('success', data['status'])

    def test_add_item_status_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        self.add_with_invalid_json('/item_statuses')

    def test_add_item_status_missing_value_json_keys(self):
        """Ensure error is thrown if the JSON
        object does not have a url key."""
        with self.client:
            response = self.client.post(
                '/item_statuses',
                data=json.dumps(dict(name=status_1)),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_item_status_missing_value_type_json_keys(self):
        """Ensure error is thrown if the JSON object
        does not have a value key."""
        with self.client:
            name = status_1
            response = self.client.post(
                '/item_statuses',
                data=json.dumps(dict(
                    name=name,
                    value=1
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_item_status_duplicate_item(self):
        """Ensure error is thrown if the item status already exists."""
        with self.client:
            name = status_1
            self.client.post(
                '/item_statuses',
                data=json.dumps(dict(
                    name=name,
                    value=1,
                    value_type='Multiplier'
                )),
                content_type='application/json',
            )
            response = self.client.post(
                '/item_statuses',
                data=json.dumps(dict(
                    name=name,
                    value=1,
                    value_type='Multiplier'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That item status already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_item_status(self):
        """Ensure get single item status behaves correctly."""
        item_status = add_item_status(status_1,
                        1,
                        'Multiplier')
        with self.client:
            response = self.client.get('/item_statuses/{0}'.format(item_status.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertTrue('updated_at' in data['data'])
            self.assertEqual(status_1, data['data']['name'])
            self.assertEqual(1, data['data']['value'])
            self.assertEqual('Multiplier', data['data']['value_type'])
            self.assertIn('success', data['status'])

    def test_single_item_status_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/item_statuses/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Item status does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_item_status_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/item_statuses/0')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Item status does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_item_statuses(self):
        """Ensure get all item statuses behaves correctly."""
        add_item_status(status_1,
                 1,
                 'Multiplier')
        
        add_item_status(status_2,
                 1,
                 'Multiplier')

        with self.client:
            response = self.client.get('/item_statuses')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['item_statuses']), 2)

            # First Item
            self.assertTrue('created_at' in data['data']['item_statuses'][0])
            self.assertTrue('updated_at' in data['data']['item_statuses'][0])
            self.assertEqual(status_1,
                          data['data']['item_statuses'][0]['name'])
            self.assertEqual(1,
                          data['data']['item_statuses'][0]['value'])
            self.assertEqual('Multiplier',
                          data['data']['item_statuses'][0]['value_type'])

            # Second Item
            self.assertTrue('created_at' in data['data']['item_statuses'][1])
            self.assertTrue('updated_at' in data['data']['item_statuses'][1])
            self.assertEqual(status_2,
                          data['data']['item_statuses'][1]['name'])
            self.assertEqual(1,
                          data['data']['item_statuses'][1]['value'])
            self.assertEqual('Multiplier',
                          data['data']['item_statuses'][1]['value_type'])

            self.assertIn('success', data['status'])

    def test_edit_item_status(self):
        """Ensure we can edit an item's status."""
        with self.client:
            name = status_1
            value = 1
            value_type = 'Multiplier'

            response = self.client.post(
                '/item_statuses',
                data=json.dumps(dict(
                    name=name,
                    value=value,
                    value_type=value_type
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('{0} was added!'.format(name), data['message'])
            self.assertIn('success', data['status'])

            # Attempt to edit the item's status
            name = status_2
            value = 2
            value_type = 'Subtraction'
            response = self.client.patch(
                '/item_statuses/{0}'.format(data['data']['id']),
                data=json.dumps(dict(
                    name=name,
                    value=value,
                    value_type=value_type
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(name, data['data']['name'])
            self.assertEqual(value, data['data']['value'])
            self.assertIn(value_type, data['data']['value_type'])

            # Verify the data was stored correctly
            response = self.client.get('/item_statuses/{0}'.format(data['data']['id']))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(name, data['data']['name'])
            self.assertEqual(value, data['data']['value'])
            self.assertIn(value_type, data['data']['value_type'])
            self.assertIn('success', data['status'])