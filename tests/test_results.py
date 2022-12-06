import unittest
import uuid

from fastapi.testclient import TestClient

from app.internal.database import database
from app.internal.logic.results.update_users import update_users
from app.internal.models.general.message import create_message
from app.main import app
from tests.mock_data.mock_results import get_standings_2022_data
from tests.mock_data.mock_users import create_user_data, create_bet_data


class TestResults(unittest.TestCase):
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

    ###############################
    # /results/race/{season}/{race} #
    ###############################

    def test_get_all_results_for_round(self):
        user_id = str(uuid.uuid4())
        data = create_user_data(user_id)

        bet_data = create_bet_data(user_id)

        database["Users"].insert_one(data)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.get(f"/results/race/2022/22").json()

        mock_data = get_standings_2022_data()

        self.assertEqual(res, mock_data)

    def test_get_all_results_for_round_404(self):
        user_id = str(uuid.uuid4())
        data = create_user_data(user_id)

        database["Users"].insert_one(data)

        res = self.test_client.get(f"/results/race/2022/22")

        error = create_message("Bets not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)

    ###############################
    # /results/standings/{season} #
    ###############################

    def test_get_standings(self):
        user_id = str(uuid.uuid4())
        data = create_user_data(user_id)

        bet_data = create_bet_data(user_id)

        database["Users"].insert_one(data)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.get(f"/results/standings/2022").json()

        mock_data = get_standings_2022_data()

        self.assertEqual(res, mock_data)

    def test_get_standings_404(self):
        user_id = str(uuid.uuid4())
        data = create_user_data(user_id)

        bet_data = create_bet_data(user_id)

        database["Users"].insert_one(data)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.get(f"/results/standings/2021")

        error = create_message("Season not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)
