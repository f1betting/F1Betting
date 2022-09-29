from pydantic import BaseModel


class Seasons(BaseModel):
    seasons: list[int]
