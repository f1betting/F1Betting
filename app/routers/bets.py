import os

import requests
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.internal.auth import decode_user
from app.internal.database import database
from app.internal.logic.errors import data_not_found
from app.internal.models.betting.bet import BetExample, BaseBet, FullBet
from app.internal.models.betting.user import User
from app.internal.models.general.message import Message, create_message

router = APIRouter(
    tags=["Bet"],
)


@router.get("/bet/{season}/{race}",
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
def get_bet(season: int, race: int, auth_user: User = Depends(decode_user)):
    # Fetch user
    user = database["Users"].find_one({"username": auth_user.username, "uuid": auth_user.uuid})

    if not user:
        return JSONResponse(status_code=404, content=create_message("User not found"))

    # Fetch bet
    bet = database["Bets"].find_one({"uuid": user["uuid"], "season": season, "round": race})

    if not bet:
        return JSONResponse(status_code=404, content=create_message("Bet not found"))

    # Return bet
    return bet


@router.post("/bet",
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
def create_bet(bet: BaseBet, auth_user: User = Depends(decode_user)):
    host = os.getenv("F1_API")

    # Fetch next event
    url = f"{host}/event/next"

    res = requests.get(url, timeout=15)
    data = res.json()

    # Capitalize driver abbreviation codes for consistency
    bet.p1 = bet.p1.upper()
    bet.p2 = bet.p2.upper()
    bet.p3 = bet.p3.upper()

    # Check for duplicates
    if bet.p1 == bet.p2 or bet.p2 == bet.p3 or bet.p1 == bet.p3:
        return JSONResponse(status_code=409, content=create_message("Duplicate drivers"))

    bet = jsonable_encoder(bet)

    # Fetch drivers
    drivers_url = f"{host}/drivers/{data['season']}"
    drivers_res = requests.get(drivers_url, timeout=15)
    drivers_data = drivers_res.json()
    drivers = drivers_data["drivers"]

    # Create array of driver abbreviation codes
    driver_codes = []

    for driver in drivers:
        driver_codes.append(driver["code"])

    # Check for invalid codes in bet
    if bet["p1"] not in driver_codes or bet["p2"] not in driver_codes or bet["p3"] not in driver_codes:
        return JSONResponse(status_code=404, content=create_message("Driver not found"))

    # Generate full bet data
    bet["season"] = data["season"]
    bet["round"] = data["round"]
    bet["points"] = 0
    bet["uuid"] = auth_user.uuid

    # Fetch user
    user = database["Users"].find_one({"username": auth_user.username, "uuid": auth_user.uuid})

    if not user:
        return JSONResponse(status_code=404, content=create_message("User not found"))

    # Check if user already has made a bet
    if list(database["Bets"].find(
            {"uuid": user["uuid"], "season": bet["season"], "round": bet["round"]})):
        return JSONResponse(status_code=409, content=create_message("Bet already exists"))

    # Add bet to database
    new_bet = database["Bets"].insert_one(bet)

    # Return bet to user
    created_bet = database["Bets"].find_one({"_id": new_bet.inserted_id})

    return created_bet


@router.put("/bet",
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
def edit_bet(p1: str, p2: str, p3: str, auth_user: User = Depends(decode_user)):
    user = database["Users"].find_one({"username": auth_user.username, "uuid": auth_user.uuid})

    if not user:
        return JSONResponse(status_code=404, content=create_message("User not found"))

    host = os.getenv("F1_API")

    # Fetch next event
    url = f"{host}/event/next"

    res = requests.get(url, timeout=15)
    data = res.json()

    # Fetch existing bet
    bet = database["Bets"].find_one({"uuid": user["uuid"], "season": data["season"], "round": data["round"]})

    if not bet:
        return JSONResponse(status_code=404, content=create_message("Bet not found"))

    host = os.getenv("F1_API")

    # Fetch drivers
    drivers_url = f"{host}/drivers/{data['season']}"
    drivers_res = requests.get(drivers_url, timeout=15)
    drivers_data = drivers_res.json()
    drivers = drivers_data["drivers"]

    # Create array of driver abbreviation codes
    driver_codes = []

    for driver in drivers:
        driver_codes.append(driver["code"])

    # Check for invalid codes
    if p1.upper() not in driver_codes or p2.upper() not in driver_codes or p3.upper() not in driver_codes:
        return data_not_found("Driver")

    # Update bet
    database["Bets"].update_one({"_id": bet["_id"]}, {"$set": {
        "p1": p1.upper(),
        "p2": p2.upper(),
        "p3": p3.upper()
    }})

    return create_message("Bet updated successfully")


@router.delete("/bet",
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
def delete_bet(auth_user: User = Depends(decode_user)):
    # Fetch user
    user = database["Users"].find_one({"username": auth_user.username, "uuid": auth_user.uuid})

    if not user:
        return data_not_found("User")

    host = os.getenv("F1_API")

    # Fetch next event
    url = f"{host}/event/next"

    res = requests.get(url, timeout=15)
    data = res.json()

    # Find bet
    bet = database["Bets"].find_one({"uuid": user["uuid"], "season": data["season"], "round": data["round"]})

    if not bet:
        return data_not_found("Bet")

    # Delete bet
    database["Bets"].delete_one({"_id": bet["_id"]})

    return create_message("Bet deleted successfully")
