from typing import Union

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic.networks import AnyUrl, IPvAnyAddress
from src.application.dependencies import Container
from src.services import GeolocationService

from .security import PROTECTED

geolocation_router = APIRouter(prefix="/localizations", dependencies=PROTECTED)


@geolocation_router.get("/")
@inject
async def get_all_saved_localizations(
    ipstack_svc: GeolocationService = Depends(Provide[Container.ipstack_service]),
):
    """
    PRIVATE ROUTE - JWT AUTH REQUIRED.
    Returns all geolocalizations currently stored in the database.
    """
    return await ipstack_svc.get_all()


@geolocation_router.get("/check")
@inject
async def check_localization_for_address(
    address: str,
    ipstack_svc: GeolocationService = Depends(Provide[Container.ipstack_service]),
):
    """
    PRIVATE ROUTE - JWT AUTH REQUIRED.
    Returns geolocalization info for provided address (URL or IP).
    If info for this address is present in the db, this info is returned.
    Otherwise, info fetched from IPStack's API is returned. If no info is found, null is returned.
    """
    return await ipstack_svc.get(address)


class AddressJson(BaseModel):
    address: Union[IPvAnyAddress, AnyUrl]


@geolocation_router.post("/add")
@inject
async def add_localization(
    body: AddressJson,
    ipstack_svc: GeolocationService = Depends(Provide[Container.ipstack_service]),
):
    """
    PRIVATE ROUTE - JWT AUTH REQUIRED.
    Fetches geolocalization info for the provided address (URL or IP, inside a JSON body) and saves it in the db.
    If an entry for the provided address already exists, it is overwritten.
    """
    return await ipstack_svc.add(body.address)


@geolocation_router.delete("/delete")
@inject
async def delete_localization(
    body: AddressJson,
    ipstack_svc: GeolocationService = Depends(Provide[Container.ipstack_service]),
):
    """
    PRIVATE ROUTE - JWT AUTH REQUIRED.
    Deletes geolocalization info for the provided address (URL or IP, inside a JSON body) from the db.
    """
    return await ipstack_svc.delete(body.address)
