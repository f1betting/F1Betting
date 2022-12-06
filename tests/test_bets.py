import unittest
import uuid

from fastapi.testclient import TestClient

from app.internal.database import database
from app.internal.models.general.message import create_message
from app.main import app
from tests.logic.mock_decode_user import mock_decode_user
from tests.mock_data.mock_bets import create_bet_data, create_bet_put_data, create_wrong_user_data
from tests.mock_data.mock_users import create_user_data


class TestUsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_client = TestClient(app)

        user_id = str(uuid.uuid4())
        cls.user_id = user_id

        mock_decode_user(user_id)

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

    ########
    # /bet #
    ########

    ###########
    # GET BET #
    ###########

    def test_get_bet(self):
        user_data = create_user_data(self.user_id)

        bet_data = create_bet_data(self.user_id)

        database["Users"].insert_one(user_data)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.get("/bet/2022/22", headers={"Authorization": "Bearer token"}).json()

        bet_data = create_bet_data(self.user_id)

        self.assertEqual(res, bet_data)

    def test_get_bet_wrong_user(self):
        user_data = create_wrong_user_data(self.user_id)

        bet_data = create_bet_data(self.user_id)

        database["Users"].insert_one(user_data)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.get("/bet/2022/22", headers={"Authorization": "Bearer token"})

        error = create_message("User not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)

    def test_get_bet_no_bet(self):
        user_data = create_user_data(self.user_id)

        database["Users"].insert_one(user_data)

        res = self.test_client.get("/bet/2022/22", headers={"Authorization": "Bearer token"})

        error = create_message("Bet not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)

    ##############
    # CREATE BET #
    ##############

    def test_create_bet(self):
        user_data = create_user_data(self.user_id)

        bet_post = {
            "p1": "ALB",
            "p2": "ALO",
            "p3": "BOT"
        }

        database["Users"].insert_one(user_data)

        res = self.test_client.post("/bet", headers={"Authorization": "Bearer token"}, json=bet_post).json()

        bet_data = create_bet_data(self.user_id)

        self.assertEqual(res, bet_data)

    def test_create_bet_wrong_driver(self):
        user_data = create_user_data(self.user_id)

        bet_post = {
            "p1": "VER",
            "p2": "ALO",
            "p3": "BOT"
        }

        database["Users"].insert_one(user_data)

        res = self.test_client.post("/bet", headers={"Authorization": "Bearer token"}, json=bet_post)

        error = create_message("Driver not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)

    def test_create_bet_wrong_user(self):
        user_data = create_wrong_user_data(self.user_id)

        bet_post = {
            "p1": "ALB",
            "p2": "ALO",
            "p3": "BOT"
        }

        database["Users"].insert_one(user_data)

        res = self.test_client.post("/bet", headers={"Authorization": "Bearer token"}, json=bet_post)

        error = create_message("User not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)

    def test_create_bet_duplicate_driver(self):
        user_data = create_user_data(self.user_id)

        bet_post = {
            "p1": "ALO",
            "p2": "ALO",
            "p3": "BOT"
        }

        database["Users"].insert_one(user_data)

        res = self.test_client.post("/bet", headers={"Authorization": "Bearer token"}, json=bet_post)

        error = create_message("Duplicate drivers")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 409)

    def test_create_bet_duplicate_bet(self):
        user_data = create_user_data(self.user_id)

        bet_post = {
            "p1": "ALB",
            "p2": "ALO",
            "p3": "BOT"
        }

        database["Users"].insert_one(user_data)

        bet_data = create_bet_data(self.user_id)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.post("/bet", headers={"Authorization": "Bearer token"}, json=bet_post)

        error = create_message("Bet already exists")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 409)

    ############
    # EDIT BET #
    ############

    def test_edit_bet(self):
        user_data = create_user_data(self.user_id)

        bet_data = create_bet_data(self.user_id)

        database["Users"].insert_one(user_data)

        bet_id = database["Bets"].insert_one(bet_data).inserted_id

        self.test_client.put("/bet?p1=ALB&p2=BOT&p3=ALO", headers={"Authorization": "Bearer token"})

        bet_data = create_bet_put_data(self.user_id)

        res = database["Bets"].find_one({"_id": bet_id}, {"_id": False})

        self.assertEqual(res, bet_data)

    def test_edit_bet_no_bet(self):
        user_data = create_user_data(self.user_id)

        database["Users"].insert_one(user_data)

        res = self.test_client.put("/bet?p1=ALB&p2=BOT&p3=ALO", headers={"Authorization": "Bearer token"})

        error = create_message("Bet not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)

    def test_edit_bet_wrong_driver(self):
        user_data = create_user_data(self.user_id)

        bet_data = create_bet_data(self.user_id)

        database["Users"].insert_one(user_data)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.put("/bet?p1=VER&p2=BOT&p3=ALO", headers={"Authorization": "Bearer token"})

        error = create_message("Driver not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)

    def test_edit_bet_wrong_user(self):
        user_data = create_wrong_user_data(self.user_id)

        bet_data = create_bet_data(self.user_id)

        database["Users"].insert_one(user_data)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.put("/bet?p1=VER&p2=BOT&p3=ALO", headers={"Authorization": "Bearer token"})

        error = create_message("User not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)

    def test_edit_bet_duplicate_driver(self):
        user_data = create_user_data(self.user_id)

        bet_data = create_bet_data(self.user_id)

        database["Users"].insert_one(user_data)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.put("/bet?p1=ALB&p2=ALB&p3=ALO", headers={"Authorization": "Bearer token"})

        error = create_message("Duplicate drivers")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 409)

    ##############
    # DELETE BET #
    ##############

    def test_delete_bet(self):
        user_data = create_user_data(self.user_id)

        bet_data = create_bet_data(self.user_id)

        database["Users"].insert_one(user_data)

        bet_id = database["Bets"].insert_one(bet_data).inserted_id

        res = self.test_client.delete("/bet", headers={"Authorization": "Bearer token"})

        msg = create_message("Bet deleted successfully")

        deleted_bet = database["Bets"].find_one({"_id": bet_id}, {"_id": False})

        self.assertIsNone(deleted_bet)
        self.assertEqual(res.json(), msg)

    def test_delete_bet_wrong_user(self):
        user_data = create_wrong_user_data(self.user_id)

        bet_data = create_bet_data(self.user_id)

        database["Users"].insert_one(user_data)

        database["Bets"].insert_one(bet_data)

        res = self.test_client.delete("/bet", headers={"Authorization": "Bearer token"})

        error = create_message("User not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)

    def test_delete_bet_no_bet(self):
        user_data = create_user_data(self.user_id)

        database["Users"].insert_one(user_data)

        res = self.test_client.delete("/bet", headers={"Authorization": "Bearer token"})

        error = create_message("Bet not found")

        self.assertEqual(res.json(), error)
        self.assertEqual(res.status_code, 404)
