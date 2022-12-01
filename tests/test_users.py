import unittest

from fastapi.testclient import TestClient

from app.main import app
from tests.mock_data.mock_users import get_all_users_data, get_user_by_id_data


class TestRoundPoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_client = TestClient(app, base_url="http://127.0.0.1:8000")

    def test_get_all_users(self):
        res = self.test_client.get("/users").json()

        mock_data = get_all_users_data()

        self.assertEqual(res, mock_data)

    def test_get_user_by_id(self):
        res = self.test_client.get("/users/1").json()

        mock_data = get_user_by_id_data()

        self.assertEqual(res, mock_data)
