import os

import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer
from google.auth.transport import requests
from google.oauth2 import id_token

from app.internal.models.betting.user import User

# SETUP OAUTH2
# https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/

token_auth_scheme = HTTPBearer()


def decode_token(token):
    request = requests.Request()

    user = id_token.verify_oauth2_token(token.credentials, request, audience=os.getenv("GOOGLE_ID"))

    return User(username=user["name"].lower(), uuid=user["sub"])


def decode_user(token: jwt = Depends(token_auth_scheme)):
    user = decode_token(token)
    return user
