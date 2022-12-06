import unittest
import uuid

from fastapi.testclient import TestClient

from app.internal.database import database
from app.internal.logic.results.update_users import update_users
from app.internal.models.general.message import create_message
from app.main import app
from tests.mock_data.mock_users import create_user_data, create_bet_data


class TestSeason(unittest.TestCase):
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

    ############
    # /seasons #
    ############

    def test_get_seasons(self):
        user_id = str(uuid.uuid4())
        data = create_user_data(user_id)

        bet_data = create_bet_data(user_id)

        database["Users"].insert_one(data)

        database["Bets"].insert_one(bet_data)

        update_users()

        res = self.test_client.get("/seasons").json()

        self.assertEqual(res["seasons"], [2022])

    def test_get_seasons_404(self):
        res = self.test_client.get("/seasons")

        error = create_message("Seasons not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)
