import json
import unittest
from datetime import datetime

from project.tests.base import BaseTestCase
from project.api.models import DXLooker
from project import db

ESM = "email_send_month"

TEST_DATE1 = datetime(2018, 8, 1).isoformat()
TEST_DATE_CHECK1 = "01 Aug 2018"

TEST_DATE2 = datetime(2018, 8, 2).isoformat()
TEST_DATE_CHECK2 = "02 Aug 2018"


def add_month(email_send_month):
    dxl = DXLooker(email_send_month)
    db.session.add(dxl)
    db.session.commit()
    return dxl


class TestDXLooker(BaseTestCase):
    """Tests for the DX Looker Service."""

    def test_dx_looker(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/dx_looker/ping")
        data = json.loads(response.data.decode())
        self.assertTrue(response.status_code, 200)
        self.assertIn("pong", data["message"])
        self.assertIn("success", data["status"])

    def test_email_send_month(self):
        """Ensure a new send month can be added to the database"""
        with self.client:
            response = self.client.post(
                "/dx_looker",
                data=json.dumps({
                    ESM: TEST_DATE1,
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn("{} was added!".format(TEST_DATE1), data["message"])
            self.assertIn("success", data["status"])

    def test_add_email_send_month_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                "/dx_looker",
                data=json.dumps({}),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_email_send_month_invalid_json_keys(self):
        """
        Ensure error is thrown if JSON does not have an email send month
        """
        with self.client:
            response = self.client.post(
                "/dx_looker",
                data=json.dumps({".net": 10}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_email_send_month_duplicate(self):
        """Ensure error is thrown if the email send month already exists."""
        with self.client:
            self.client.post(
                "/dx_looker",
                data=json.dumps({
                    ESM: TEST_DATE1
                }),
                content_type="application/json"
            )
            response = self.client.post(
                "/dx_looker",
                data=json.dumps(
                    {ESM: TEST_DATE1}
                ),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("That {} already exists.".format(ESM),
                          data["message"])

    def test_single_month(self):
        """Ensure get single month behaves correctly."""
        dxl = add_month(TEST_DATE1)
        with self.client:
            response = self.client.get(
                "/dx_looker/{}".format(dxl.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(TEST_DATE_CHECK1, data["data"][ESM])
            self.assertIn("success", data["status"])

    def test_single_month_no_id(self):
        """Ensure error is thrown if an id is not provided"""
        with self.client:
            response = self.client.get("/dx_looker/no_id")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("{} does not exist".format(ESM), data["message"])
            self.assertIn("fail", data["status"])

    def test_single_month_incorrect_id(self):
        """Ensure error is thrown if the id does not exist"""
        with self.client:
            response = self.client.get("/dx_looker/99999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("{} does not exist".format(ESM), data["message"])
            self.assertIn("fail", data["status"])

    def test_all_months(self):
        """Ensure get all months behaves correctly"""
        add_month(TEST_DATE1)
        add_month(TEST_DATE2)
        with self.client:
            response = self.client.get("/dx_looker")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["rows"]), 2)
            self.assertIn(TEST_DATE_CHECK1, data["data"]["rows"][0][ESM])
            self.assertIn(TEST_DATE_CHECK2, data["data"]["rows"][1][ESM])


if __name__ == "__main__":
    unittest.main()
