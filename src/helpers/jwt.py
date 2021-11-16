from datetime import timedelta
from typing import Dict

from src.domain import UserId
from src.settings import Settings

import jwt

from .dates import utcnow

ALGORITHM = "HS256"
EXPIRATION_TIME_SECONDS = 20 * 60


def sign_jwt(user_id: UserId) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "exp": utcnow() + timedelta(seconds=EXPIRATION_TIME_SECONDS),
    }

    return jwt.encode(payload, Settings().JWT_SECRET, algorithm=ALGORITHM)


def get_user_id_from_token(token: str) -> UserId:
    try:
        payload = jwt.decode(token, Settings().JWT_SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError as e:
        raise InvalidTokenException()

    user_id = payload.get("user_id")
    if not user_id:
        raise InvalidTokenException()

    return user_id


class JwtTokenException(Exception):
    pass


class InvalidTokenException(JwtTokenException):
    pass
