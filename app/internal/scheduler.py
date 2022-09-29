import os

import requests
from rocketry import Rocketry

from app.internal.database import database
from app.internal.logic.results.get_points import get_points

app = Rocketry(config={'task_execution': 'async'})


@app.task("every 60 seconds")
def update_users():
    ip = os.getenv("F1_API")

    seasons = list(database["Bets"].find().distinct("season"))

    for season in seasons:
        races = list(database["Bets"].find({"season": season}).distinct("round"))

        for race in races:
            bets = list(database["Bets"].find({"round": race}))

            race_url = f"http://{ip}/results/race/{season}/{race}"
            race_res = requests.get(race_url)
            results = race_res.json()

            if "results" in results.keys():
                for bet in bets:
                    round_points = get_points(results["results"], bet)

                    database["Bets"].update_one({"uuid": bet["uuid"], "round": race}, {"$set": {
                        "points": round_points
                    }})

        users = list(database["Users"].find({}, {"_id": False}).sort("points", -1))

        for user in users:
            all_bets = list(database["Bets"].find({"uuid": user["uuid"], "season": season}))

            all_points = 0

            for bet in all_bets:
                all_points += bet["points"]

            database["Users"].update_one({"uuid": user["uuid"]}, {"$set": {
                f"points_{season}": all_points
            }})
