from dataclasses import dataclass
from typing import List, Optional, Union

from pydantic import AnyUrl, BaseModel, IPvAnyAddress
from src.domain.geolocation import Geolocation
from src.helpers.exceptions import HttpClientError, map_pydantic_errors_to_http
from src.helpers.http_client import HttpClient
from src.repositories.geolocation import GeolocationRepository


class Address(BaseModel):
    address: Union[IPvAnyAddress, AnyUrl]


@dataclass(frozen=True)
class GeolocationService:
    http_client: HttpClient
    geolocation_repo: GeolocationRepository

    async def get_all(self) -> List[Geolocation]:
        return await self.geolocation_repo.get_all()

    async def get(self, raw_address: str) -> Optional[Geolocation]:
        with map_pydantic_errors_to_http():
            validated_address_obj = Address(address=raw_address)

        entry_in_db = await self.geolocation_repo.get(
            str(validated_address_obj.address)
        )
        if not entry_in_db:
            # no try/except clause for API error; we let it propagate
            return await self.http_client.get_geolocation_for_address(
                validated_address_obj.address
            )

        return entry_in_db

    async def add(self, raw_address: str) -> Geolocation:
        with map_pydantic_errors_to_http():
            validated_address_obj = Address(address=raw_address)

        data = await self.http_client.get_geolocation_for_address(
            validated_address_obj.address
        )

        return await self.geolocation_repo.create(data.dict())

    async def delete(self, raw_address: str) -> Geolocation:
        validated_address = Address(address=raw_address)
        return await self.geolocation_repo.delete(str(validated_address.address))
