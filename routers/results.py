import requests
from dotenv import dotenv_values
from fastapi import APIRouter
from fastapi.responses import JSONResponse

import main
from internal.logic.results.get_points import get_points
from internal.models.betting.user_results import UserResults, UserResultExample
from internal.models.general.message import Message, create_message

config = dotenv_values(".env")

router = APIRouter(
    prefix="/results",
    tags=["Results"],
)


@router.get("/race/{season}/{race}",
            response_model=UserResults,
            responses={
                404: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("Users not found")
                    }
                }},
                200: {"model": UserResults, "content": {
                    "application/json": {
                        "example": {
                            "results": [
                                UserResultExample
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
        round_points = get_points(results, bet)

        main.app.database["Bets"].update_one({"username": bet["username"]}, {"$set": {
            "points": round_points
        }})

    bets = list(main.app.database["Bets"].find({"season": season, "round": race},
                                               {"_id": 0, "p1": 0, "p2": 0, "p3": 0, "season": 0, "round": 0}))

    if not bets:
        return JSONResponse(status_code=404, content=create_message("Bets not found"))

    return {"results": bets}


@router.put("/race/{season}/{race}",
            response_model=UserResults,
            responses={
                404: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("Users not found")
                    }
                }},
                200: {"model": UserResults, "content": {
                    "application/json": {
                        "example": {
                            "results": [
                                UserResultExample
                            ]
                        }
                    }
                }}
            })
def update_users_for_round(season: int, race: int):
    bets = list(main.app.database["Bets"].find({"round": race}))

    if not bets:
        return JSONResponse(status_code=404, content=create_message("Users not found"))

    ip = config["F1_API"]

    url = f"http://{ip}/results/race/{season}/{race}"
    res = requests.get(url)
    results = res.json()
    results = results["results"]

    for bet in bets:
        round_points = get_points(results, bet)

        user = main.app.database["Users"].find_one({"username": bet["username"]})

        main.app.database["Bets"].update_one({"username": bet["username"]}, {"$set": {
            "points": round_points
        }})

        main.app.database["Users"].update_one({"username": bet["username"]}, {"$set": {
            "points": user["points"] + round_points
        }})

    users = list(main.app.database["Users"].find({}, {"_id": False}).sort("points", -1))

    if not users:
        return JSONResponse(status_code=404, content=create_message("Users not found"))

    return {"results": users}


@router.get("/standings",
            response_model=UserResults,
            responses={
                404: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("Users not found")
                    }
                }},
                200: {"model": UserResults, "content": {
                    "application/json": {
                        "example": {
                            "results": [
                                UserResultExample
                            ]
                        }
                    }
                }}
            })
def get_standings():
    users = list(main.app.database["Users"].find({}, {"_id": False, "uuid": False}).sort("points", -1))

    if not users:
        return JSONResponse(status_code=404, content=create_message("Users not found"))

    return {"results": users}
