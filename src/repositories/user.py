from dataclasses import dataclass
from typing import Any, Dict, Optional

from sqlalchemy import select
from sqlalchemy.sql.expression import insert
from src.domain.user import User, UserId
from src.repositories.base import BaseRepository

from ._db_schema import users


@dataclass(frozen=True)
class UserRepository(BaseRepository):
    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        query = select([users]).where(users.c.id == user_id)

        row = await self.db.fetch_one(query)
        return User(**row) if row else None

    async def get_by_username(self, username: str) -> Optional[User]:
        query = select([users]).where(users.c.username == username)

        row = await self.db.fetch_one(query)
        return User(**row) if row else None

    async def create(self, input_: Dict[str, Any]) -> User:
        query = insert(users).values(**input_).returning(users)

        row = await self.db.fetch_one(query)
        return User(**row) if row else None
