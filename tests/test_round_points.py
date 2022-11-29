import unittest

from app.internal.logic.results.get_points import get_points
from tests.mock_data.mock_2022_21_results import get_2022_22_results, get_2022_22_correct_bet, \
    get_2022_22_incorrect_bet


class TestRoundPoints(unittest.TestCase):
    def test_round_points_correct(self):
        results = get_2022_22_results()

        round_points = get_points(results["results"], get_2022_22_correct_bet())

        self.assertEqual(round_points, 6)

    def test_round_points_p1correct(self):
        results = get_2022_22_results()

        round_points = get_points(results["results"], get_2022_22_incorrect_bet())

        self.assertEqual(round_points, 0)
