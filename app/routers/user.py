import uuid

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.internal.database import database
from app.internal.logic.errors import data_not_found
from app.internal.models.betting.user import UserExample, User, Users, UserPointsExample
from app.internal.models.general.message import Message, create_message

router = APIRouter(
    tags=["Users"],
)


@router.get("/users",
            response_model=Users,
            responses={
                404: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("Users not found")
                    }
                }},
                200: {"model": Users, "content": {
                    "application/json": {
                        "example": {
                            "users": [
                                UserExample
                            ]
                        }
                    }
                }}
            })
def get_all_users():
    users = list(database["Users"].find({}, {"_id": 0}))

    if not users:
        return data_not_found("Users")

    return {"users": users}


@router.get("/users/{user_id}",
            responses={
                404: {"model": Message, "content": {
                    "application/json": {
                        "example": create_message("User not found")
                    }
                }},
                200: {"model": User, "content": {
                    "application/json": {
                        "example": UserPointsExample
                    }
                }}
            })
def get_user_by_id(user_id: str):
    # Fetch user
    user = database["Users"].find_one({"uuid": user_id}, {"_id": 0})

    if not user:
        return data_not_found("User")

    return user


@router.post("/users",
             response_model=User,
             responses={
                 409: {"model": Message, "content": {
                     "application/json": {
                         "example": create_message("User already exists")
                     }
                 }},
                 200: {"model": User, "content": {
                     "application/json": {
                         "example": UserExample
                     }
                 }}
             })
def create_user(user: User):
    # Convert username to lowercase for consistency
    user.username = user.username.lower()

    user = jsonable_encoder(user)

    # Generate UUID if not provided
    if not user["uuid"]:
        user["uuid"] = str(uuid.uuid4())

    # Check if UUID already exists
    if list(database["Users"].find({"uuid": user["uuid"]})):
        return JSONResponse(status_code=409, content=create_message("User already exists"))

    # Create new user
    new_user = database["Users"].insert_one(user)

    # Return created user
    created_user = database["Users"].find_one({"_id": new_user.inserted_id})

    return created_user
