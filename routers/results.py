from dotenv import dotenv_values
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from internal.database import database
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
    bets = list(database["Bets"].find({"season": season, "round": race},
                                      {"_id": 0, "p1": 0, "p2": 0, "p3": 0, "season": 0, "round": 0}))

    if not bets:
        return JSONResponse(status_code=404, content=create_message("Bets not found"))

    for bet in bets:
        user = database["Users"].find_one({"uuid": bet["uuid"]})

        bet["username"] = user["username"]

    return {"results": bets}


@router.get("/standings/{season}",
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
def get_standings(season: int):
    users = list(database["Users"].find({}, {"_id": False, "uuid": False}).sort(f"points_{season}", -1))

    seasons = list(database["Bets"].find().distinct("season"))

    if season not in seasons:
        return JSONResponse(status_code=404, content=create_message("Season not found"))

    if not users:
        return JSONResponse(status_code=404, content=create_message("Users not found"))

    for user in users:
        user["points"] = user[f"points_{season}"]

    return {"results": users}
