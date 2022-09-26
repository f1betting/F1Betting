import requests
from dotenv import dotenv_values
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from internal.auth import decode_user
from internal.database import database
from internal.logic.results.get_points import get_points
from internal.models.betting.user import BaseUser
from internal.models.betting.user_results import UserResults, UserResultExample, UserResult
from internal.models.general.message import Message, create_message
from routers.user import get_user_by_id

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
    bets = list(database["Bets"].find({"season": season, "round": race},
                                      {"_id": 0, "p1": 0, "p2": 0, "p3": 0, "season": 0, "round": 0}))

    if not bets:
        return JSONResponse(status_code=404, content=create_message("Bets not found"))

    for bet in bets:
        user = database["Users"].find_one({"uuid": bet["uuid"]})

        bet["username"] = user["username"]

    return {"results": bets}


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
    users = list(database["Users"].find({}, {"_id": False, "uuid": False}).sort("points", -1))

    if not users:
        return JSONResponse(status_code=404, content=create_message("Users not found"))

    return {"results": users}
