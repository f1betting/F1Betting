from dotenv import dotenv_values
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from internal.database import database
from internal.models.betting.season import Seasons
from internal.models.general.message import Message, create_message

config = dotenv_values(".env")

router = APIRouter(
    tags=["Seasons"],
)


@router.get("/seasons",
            response_model=Seasons,
            responses={
                404: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("Users not found")
                    }
                }},
                200: {"model": Seasons, "content": {
                    "application/json": {
                        "example": {
                            "seasons": [
                                2022
                            ]
                        }
                    }
                }}
            })
def get_seasons():
    seasons = list(database["Bets"].find().distinct("season"))

    if not seasons:
        return JSONResponse(status_code=404, content=create_message("Seasons not found"))

    seasons.sort(reverse=True)

    return {"seasons": seasons}
