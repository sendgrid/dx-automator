import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Looker


def add_user(username, email):
    user = Looker(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestLookerService(BaseTestCase):
    """Tests for the Users Service."""

    def test_looker(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/looker/ping")
        data = json.loads(response.data.decode())
        self.assertTrue(response.status_code, 200)
        self.assertIn("pong", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added to the database"""
        with self.client:
            response = self.client.post(
                "/looker",
                data=json.dumps({
                    "username": "james",
                    "email": "james@sendgrid.com"
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn("james@sendgrid.com was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                "/looker",
                data=json.dumps({}),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key
        """
        with self.client:
            response = self.client.post(
                "/looker",
                data=json.dumps({"email": "james@sendgrid.com"}),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                "/looker",
                data=json.dumps({
                    "username": "james",
                    "email": "james@sendgrid.com"
                }),
                content_type="application/json"
            )
            response = self.client.post(
                "/looker",
                data=json.dumps({
                    "username": "james",
                    "email": "james@sendgrid.com"
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                "Sorry. That email already exists.",
                data["message"]
            )
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single user behaves correctly"""
        user = add_user(username="james", email="james@sendgrid.com")
        with self.client:
            response = self.client.get("/looker/{}".format(user.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("james", data["data"]["username"])
            self.assertIn("james@sendgrid.com", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get("/looker/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist"""
        with self.client:
            response = self.client.get("/looker/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user("james", "james@sendgrid.com")
        add_user("purpura", "purpura@sendgrid.com")
        with self.client:
            response = self.client.get("/looker")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertIn("james", data["data"]["users"][0]["username"])
            self.assertIn("james@sendgrid.com", data["data"]["users"][0]["email"])
            self.assertIn("purpura", data["data"]["users"][1]["username"])
            self.assertIn("purpura@sendgrid.com", data["data"]["users"][1]["email"])
            self.assertIn("success", data["status"])


if __name__ == "__main__":
    unittest.main()
