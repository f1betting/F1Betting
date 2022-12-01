from fastapi import APIRouter

from app.internal.database import database
from app.internal.logic.errors import data_not_found
from app.internal.models.betting.season import Seasons
from app.internal.models.general.message import Message, create_message

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
    # Fetch all unique seasons
    seasons = list(database["Bets"].find().distinct("season"))

    if not seasons:
        return data_not_found("Seasons")

    # Sort seasons
    seasons.sort(reverse=True)

    return {"seasons": seasons}
