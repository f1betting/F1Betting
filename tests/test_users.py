import unittest
import uuid

from fastapi.testclient import TestClient

from app.internal.database import database
from app.internal.logic.results.update_users import update_users
from app.main import app
from tests.mock_data.mock_users import get_all_users_data, get_user_by_id_data, create_user_data, create_bet_data


class TestRoundPoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_client = TestClient(app)

    @classmethod
    def setUp(cls):
        database.drop_collection("Users")
        database.create_collection("Users")

        database.drop_collection("Bets")
        database.create_collection("Bets")

    @classmethod
    def tearDown(cls):
        database.drop_collection("Users")
        database.drop_collection("Bets")

    def test_get_all_users(self):
        user_id = str(uuid.uuid4())
        data = create_user_data(user_id)

        database["Users"].insert_one(data)

        res = self.test_client.get("/users").json()

        mock_data = get_all_users_data(user_id)

        self.assertEqual(res, mock_data)

    def test_get_user_by_id(self):
        user_id = str(uuid.uuid4())
        data = create_user_data(user_id)

        bet_data = create_bet_data(user_id)

        database["Users"].insert_one(data)

        database["Bets"].insert_one(bet_data)

        # TODO: F1 API MOCKING
        update_users()

        res = self.test_client.get(f"/users/{user_id}").json()

        mock_data = get_user_by_id_data(user_id)

        self.assertEqual(res, mock_data)

    def test_create_user(self):
        user_id = str(uuid.uuid4())
        data = create_user_data(user_id)

        res = self.test_client.post("/users", json=data).json()

        created_user = database["Users"].find_one({"uuid": user_id}, {"_id": False})

        self.assertTrue(res == data == created_user)
