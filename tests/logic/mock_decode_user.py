from unittest.mock import Mock

from app.internal.auth import Auth
from app.internal.models.betting.user import User


def mock_decode_user(user_id):
    auth_decode_token_mock = Mock()
    user = {
        "sub": user_id,
        "name": "test_user",
    }
    auth_decode_token_mock.return_value = User(username=user["name"].lower(), uuid=user["sub"])

    auth_class = Auth
    auth_class.decode_token = auth_decode_token_mock