from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.internal.database import database
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
        return JSONResponse(status_code=404, content=create_message("Seasons not found"))

    # Sort seasons
    seasons.sort(reverse=True)

    return {"seasons": seasons}
