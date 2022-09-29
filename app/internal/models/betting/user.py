import uuid

from pydantic import BaseModel


class User(BaseModel):
    username: str
    uuid: str | None


class Users(BaseModel):
    users: list[User]


UserExample = {
    "username": "Niek",
    "uuid": uuid.uuid4(),
}

UserPointsExample = {
    "username": "niek",
    "uuid": uuid.uuid4(),
    "points_2022": 19
}
