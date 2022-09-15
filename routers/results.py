import requests
from dotenv import dotenv_values
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import main
from classes.betting.bet import FullBet, BetExample, BetResults
from classes.betting.user import UserExample, BaseUser, FullUser, Users
from classes.general.message import Message, create_message

config = dotenv_values(".env")

router = APIRouter(
    prefix="/results",
    tags=["Results"],
)


@router.get("/{season}/{race}",
            response_model=BetResults,
            responses={
                404: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("Users not found")
                    }
                }},
                200: {"model": Users, "content": {
                    "application/json": {
                        "example": {
                            "results": [
                                BetExample
                            ]
                        }
                    }
                }}
            })
def get_all_results_for_round(season: int, race: int):
    bets = list(main.app.database["Bets"].find({"round": race}))

    if not bets:
        return JSONResponse(status_code=404, content=create_message("Users not found"))

    ip = config["F1_API"]

    url = f"http://{ip}/results/race/{season}/{race}"
    res = requests.get(url)
    results = res.json()
    results = results["results"]

    for bet in bets:
        round_points = 0

        for result in results:
            print(result)

            if result["position"] < 4:
                if result["Driver"]["code"] == bet["p1"]:
                    round_points += 3

                if result["Driver"]["code"] == bet["p2"]:
                    round_points += 2

                if result["Driver"]["code"] == bet["p3"]:
                    round_points += 1

        user = main.app.database["Users"].find_one({"username": bet["username"]})

        main.app.database["Bets"].update_one({"username": bet["username"]}, {"$set": {
            "points": round_points
        }})

        main.app.database["Users"].update_one({"username": bet["username"]}, {"$set": {
            "points": user["points"] + round_points
        }})

    bets = list(main.app.database["Bets"].find({"season": season, "round": race}))

    if not bets:
        return JSONResponse(status_code=404, content=create_message("Bets not found"))

    for bet in bets:
        del bet["_id"]

    return {"results": bets}
