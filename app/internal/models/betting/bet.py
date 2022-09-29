from pydantic import BaseModel


class BaseBet(BaseModel):
    p1: str
    p2: str
    p3: str


class FullBet(BaseBet):
    uuid: str
    season: int
    round: int
    points: int


class BetResults(BaseModel):
    results: list[FullBet]


BetExample = {
    "uuid": "123712308762698123",
    "p1": "RUS",
    "p2": "LEC",
    "p3": "RUS",
    "season": 2022,
    "round": 16,
    "points": 2
}
