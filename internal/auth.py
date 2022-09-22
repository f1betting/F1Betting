import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer

from internal.models.betting.user import BaseUser

# SETUP OAUTH2
# https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/

token_auth_scheme = HTTPBearer()


def decode_token(token):
    token = token.credentials
    user = jwt.decode(token, options={"verify_signature": False})
    return BaseUser(username=user["name"].lower(), uuid=user["sub"])


def decode_user(token: str = Depends(token_auth_scheme)):
    user = decode_token(token)
    return user
