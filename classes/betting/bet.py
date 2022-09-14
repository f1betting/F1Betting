from pydantic import BaseModel

from classes.betting.user import FullUser


class BaseBet(BaseModel):
    username: str
    p1: str
    p2: str
    p3: str


class FullBet(BaseModel):
    user: FullUser
    season: int
    round: int
    p1: str
    p2: str
    p3: str


BetExample = {
    "username": "Niek",
    "season": 2022,
    "round": 16,
    "p1": "VER",
    "p2": "LEC",
    "p3": "RUS",
}
