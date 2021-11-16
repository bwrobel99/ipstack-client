from dependency_injector import containers, providers
from src.helpers.http_client import HttpClient
from src.repositories import UserRepository
from src.repositories.geolocation import GeolocationRepository
from src.services import AuthService, GeolocationService

from .database import DatabaseResource


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    db = providers.Resource(DatabaseResource, db_url=config.DATABASE_URL)
    http_client = providers.Factory(HttpClient, _api_key=config.IPSTACK_API_KEY)

    user_repository = providers.Factory(UserRepository, db=db)
    geolocation_repository = providers.Factory(GeolocationRepository, db=db)

    auth_service = providers.Factory(AuthService, user_repo=user_repository)
    ipstack_service = providers.Factory(
        GeolocationService,
        http_client=http_client,
        geolocation_repo=geolocation_repository,
    )
