import requests
from dotenv import dotenv_values
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from database import db
from internal.models.betting.bet import BetExample, BaseBet, FullBet
from internal.models.general.message import Message, create_message

config = dotenv_values(".env")

router = APIRouter(
    prefix="/bet",
    tags=["Bet"],
)


@router.get("/{username}/{race}",
            response_model=FullBet,
            responses={
                404: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("User not found"),
                    }
                }},
                200: {"model": FullBet, "content": {
                    "application/json": {
                        "example": BetExample
                    }
                }},
            })
def get_bet(username: str, race: int):
    user = db.database["Users"].find_one({"username": username.lower()})

    if not user:
        return JSONResponse(status_code=404, content=create_message("User not found"))

    bet = db.database["Bets"].find_one({"username": user["username"], "round": race})

    if not bet:
        return JSONResponse(status_code=404, content=create_message("Bet not found"))

    return bet


@router.post("/",
             response_model=FullBet,
             responses={
                 404: {"model": Message, "content": {
                     "application/json": {
                         "example": create_message("User not found")
                     }
                 }},
                 409: {"model": Message, "content": {
                     "application/json": {
                         "example": create_message("Bet already exists")
                     }
                 }},
                 200: {"model": FullBet, "content": {
                     "application/json": {
                         "example": BetExample
                     }
                 }}
             })
def create_bet(bet: BaseBet):
    ip = config["F1_API"]

    url = f"http://{ip}/event/next"

    res = requests.get(url)
    data = res.json()

    bet.username = bet.username.lower()
    bet.p1 = bet.p1.upper()
    bet.p2 = bet.p2.upper()
    bet.p3 = bet.p3.upper()

    if bet.p1 == bet.p2 or bet.p2 == bet.p3 or bet.p1 == bet.p3:
        return JSONResponse(status_code=409, content=create_message("Duplicate drivers"))

    bet = jsonable_encoder(bet)

    drivers_url = f"http://{ip}/drivers/{data['season']}"
    drivers_res = requests.get(drivers_url)
    drivers_data = drivers_res.json()
    drivers = drivers_data["drivers"]

    driver_codes = []

    for driver in drivers:
        driver_codes.append(driver["code"])

    if not bet["p1"] in driver_codes or not bet["p2"] in driver_codes or not bet["p3"] in driver_codes:
        return JSONResponse(status_code=404, content=create_message("Driver not found"))

    bet["season"] = data["season"]
    bet["round"] = data["round"]
    bet["points"] = 0

    user = db.database["Users"].find_one({"username": bet["username"]})

    if not user:
        return JSONResponse(status_code=404, content=create_message("User not found"))

    if list(db.database["Bets"].find(
            {"username": user["username"], "season": bet["season"], "round": bet["round"]})):
        return JSONResponse(status_code=409, content=create_message("Bet already exists"))

    new_bet = db.database["Bets"].insert_one(bet)

    created_bet = db.database["Bets"].find_one({"_id": new_bet.inserted_id})

    return created_bet


@router.put("/{username}/{race}",
            response_model=Message,
            responses={
                404: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("User not found"),
                    }
                }},
                200: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("Bet updated successfully")
                    }
                }},
            })
def edit_bet(username: str, race: int, season: int, p1: str, p2: str, p3: str):
    user = db.database["Users"].find_one({"username": username.lower()})

    if not user:
        return JSONResponse(status_code=404, content=create_message("User not found"))

    bet = db.database["Bets"].find_one({"username": user["username"], "round": race, "season": season})

    if not bet:
        return JSONResponse(status_code=404, content=create_message("Bet not found"))

    ip = config["F1_API"]

    drivers_url = f"http://{ip}/drivers/{season}"
    drivers_res = requests.get(drivers_url)
    drivers_data = drivers_res.json()
    drivers = drivers_data["drivers"]

    driver_codes = []

    for driver in drivers:
        driver_codes.append(driver["code"])

    if not p1.upper() in driver_codes or not p2.upper() in driver_codes or not p3.upper() in driver_codes:
        return JSONResponse(status_code=404, content=create_message("Driver not found"))

    db.database["Bets"].update_one({"_id": bet["_id"]}, {"$set": {
        "p1": p1.upper(),
        "p2": p2.upper(),
        "p3": p3.upper()
    }})

    return create_message("Bet updated successfully")


@router.delete("/{username}/{race}",
               response_model=Message,
               responses={
                   404: {"model": Message, "content": {
                       "application/json": {
                           "example": create_message("User not found")

                       }
                   }},
                   200: {"model": Message, "content": {
                       "application/json": {
                           "example": create_message("Bet deleted successfully")
                       }
                   }},
               })
def delete_bet(username: str, race: int):
    user = db.database["Users"].find_one({"username": username.lower()})

    if not user:
        return JSONResponse(status_code=404, content=create_message("User not found"))

    bet = db.database["Bets"].find_one({"username": user["username"], "round": race})

    if not bet:
        return JSONResponse(status_code=404, content=create_message("Bet not found"))

    db.database["Bets"].delete_one({"_id": bet["_id"]})

    return create_message("Bet deleted successfully")
