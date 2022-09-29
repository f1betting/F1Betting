import uuid

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.internal.database import database
from app.internal.models.betting.user import UserExample, User, Users, UserPointsExample
from app.internal.models.general.message import Message, create_message

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/",
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
        return JSONResponse(status_code=404, content=create_message("Users not found"))

    return {"users": users}


@router.get("/{user_id}",
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
    user = database["Users"].find_one({"uuid": user_id}, {"_id": 0})

    if not user:
        return JSONResponse(status_code=404, content=create_message("User not found"))

    return user


@router.post("/",
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
    user.username = user.username.lower()

    user = jsonable_encoder(user)

    if not user["uuid"]:
        user["uuid"] = str(uuid.uuid4())

    if list(database["Users"].find({"uuid": user["uuid"]})):
        return JSONResponse(status_code=409, content=create_message("User already exists"))

    new_user = database["Users"].insert_one(user)

    created_user = database["Users"].find_one({"_id": new_user.inserted_id})

    return created_user