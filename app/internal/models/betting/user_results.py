from pydantic import BaseModel


class UserResult(BaseModel):
    username: str
    points: int


class UserResults(BaseModel):
    results: list[UserResult]


UserResultExample = {
    "username": "Niek",
    "points": 20
}
