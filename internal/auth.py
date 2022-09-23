import jwt
from dotenv import dotenv_values
from fastapi import Depends
from fastapi.security import HTTPBearer
from google.auth.transport import requests
from google.oauth2 import id_token

from internal.models.betting.user import BaseUser

# SETUP OAUTH2
# https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/

token_auth_scheme = HTTPBearer()

config = dotenv_values(".env")


def decode_token(token):
    request = requests.Request()

    user = id_token.verify_oauth2_token(token.credentials, request, audience=config["GOOGLE_ID"])

    return BaseUser(username=user["name"].lower(), uuid=user["sub"])


def decode_user(token: jwt = Depends(token_auth_scheme)):
    user = decode_token(token)
    return user
