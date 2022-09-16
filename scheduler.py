import requests
from dotenv import dotenv_values
from rocketry import Rocketry

from database import db
from internal.logic.results.get_points import get_points

config = dotenv_values(".env")

app = Rocketry()


@app.task("every 60 seconds")
def update_users():
    ip = config["F1_API"]

    url = f"http://{ip}/event/next"
    res = requests.get(url)
    data = res.json()

    season = data["season"]
    race = data["round"] - 1

    bets = list(db.database["Bets"].find({"round": race}))

    url = f"http://{ip}/results/race/{season}/{race}"
    res = requests.get(url)
    results = res.json()
    results = results["results"]

    for bet in bets:
        round_points = get_points(results, bet)

        db.database["Bets"].update_one({"username": bet["username"]}, {"$set": {
            "points": round_points
        }})

    users = list(db.database["Users"].find({}, {"_id": False}).sort("points", -1))

    for user in users:
        all_bets = list(db.database["Bets"].find({"username": user["username"], "season": season}))

        all_points = 0

        for bet in all_bets:
            all_points += bet["points"]

        db.database["Users"].update_one({"username": user["username"]}, {"$set": {
            "points": all_points
        }})
