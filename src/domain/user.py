from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, NewType

from src.domain.base import TimestampedModel

UserId = NewType("UserId", int)


class User(TimestampedModel):
    id: UserId
    username: str
    password_hash: str
