from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from sqlalchemy import or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.expression import delete
from src.domain.geolocation import Geolocation
from src.repositories.base import BaseRepository

from ._db_schema import geolocation, GEOLOCATION_IP_UNIQUE_CONSTRAINT


@dataclass(frozen=True)
class GeolocationRepository(BaseRepository):
    async def get(self, address: str) -> Optional[Geolocation]:
        query = select([geolocation]).where(
            or_(geolocation.c.ip == address, geolocation.c.url == address)
        )

        row = await self.db.fetch_one(query)
        return Geolocation(**row) if row else None

    async def get_all(self) -> List[Geolocation]:
        query = select([geolocation])

        rows = await self.db.fetch_all(query)
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

        row = await self.db.fetch_one(query)
        return Geolocation(**row)

    async def delete(self, address: str) -> Optional[Geolocation]:
        query = (
            delete(geolocation)
            .where(or_(geolocation.c.ip == address, geolocation.c.url == address))
            .returning(geolocation)
        )

        row = await self.db.fetch_one(query)
        return Geolocation(**row) if row else None
