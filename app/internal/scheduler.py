import os

import requests
from rocketry import Rocketry

from app.internal.database import database
from app.internal.logic.results.get_points import get_points

app = Rocketry(config={'task_execution': 'async'})


# This task updates the points for every user every hour.

@app.task("every 1 hours")
def update_users():
    host = os.getenv("F1_API")

    # Fetch every season the user has placed a bet for
    seasons = list(database["Bets"].find().distinct("season"))

    for season in seasons:
        # Fetch every race of the season the user has placed a bet for
        races = list(database["Bets"].find({"season": season}).distinct("round"))

        for race in races:
            # Fetch the bet of the race
            bets = list(database["Bets"].find({"round": race}))

            # Fetch the race results
            race_url = f"{host}/results/race/{season}/{race}"
            race_res = requests.get(race_url)
            results = race_res.json()

            if "results" in results.keys():
                for bet in bets:
                    # Calculate the amount points for the bet
                    round_points = get_points(results["results"], bet)

                    # Update amount of points for the bet
                    database["Bets"].update_one({"uuid": bet["uuid"], "round": race}, {"$set": {
                        "points": round_points
                    }})

        # Fetch all users
        users = list(database["Users"].find({}, {"_id": False}).sort("points", -1))

        for user in users:
            # Fetch all bets for the user
            all_bets = list(database["Bets"].find({"uuid": user["uuid"], "season": season}))

            all_points = 0

            for bet in all_bets:
                # Add points of all the bets to the user
                all_points += bet["points"]

            # Update the user with all points
            database["Users"].update_one({"uuid": user["uuid"]}, {"$set": {
                f"points_{season}": all_points
            }})
