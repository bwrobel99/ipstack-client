from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from asyncpg.exceptions import PostgresError
from sqlalchemy import or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.expression import delete
from src.domain.geolocation import Geolocation
from src.helpers.exceptions import DatabaseError
from src.repositories.base import BaseRepository

from ._db_schema import GEOLOCATION_IP_UNIQUE_CONSTRAINT, geolocation


@dataclass(frozen=True)
class GeolocationRepository(BaseRepository):
    async def get(self, address: str) -> Optional[Geolocation]:
        query = select([geolocation]).where(
            or_(geolocation.c.ip == address, geolocation.c.url == address)
        )

        try:
            row = await self.db.fetch_one(query)
        except PostgresError:
            raise DatabaseError()
        return Geolocation(**row) if row else None

    async def get_all(self) -> List[Geolocation]:
        query = select([geolocation])

        try:
            rows = await self.db.fetch_all(query)
        except PostgresError:
            raise DatabaseError()
        return [Geolocation(**row) for row in rows]

    async def create(self, input_: Dict[str, Any]) -> Geolocation:
        query = (
            insert(geolocation)
            .values(**input_)
            .on_conflict_do_update(
                constraint=GEOLOCATION_IP_UNIQUE_CONSTRAINT,
                set_={k: v for k, v in input_.items() if k != "created_at"},
            )
            .returning(geolocation)
        )

        try:
            row = await self.db.fetch_one(query)
        except PostgresError:
            raise DatabaseError()
        return Geolocation(**row)

    async def delete(self, address: str) -> Optional[Geolocation]:
        query = (
            delete(geolocation)
            .where(or_(geolocation.c.ip == address, geolocation.c.url == address))
            .returning(geolocation)
        )

        try:
            row = await self.db.fetch_one(query)
        except PostgresError:
            raise DatabaseError()

        return Geolocation(**row) if row else None
