from json import dumps

from fastapi import FastAPI, Response

from src.application import routers
from src.application.dependencies import Container

from .application.bootstrap import create_start_app_handler, create_stop_app_handler
from .application.routers import auth_router, geolocation_router
from .settings import Settings

settings = Settings()


def init_container() -> None:
    container = Container()
    container.config.from_pydantic(settings)
    container.wire(packages=[routers])


def get_app() -> FastAPI:
    init_container()

    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(geolocation_router)

    app.add_event_handler("startup", create_start_app_handler(app))
    app.add_event_handler("shutdown", create_stop_app_handler(app))

    return app


app = get_app()


@app.route("/")
def healthcheck(*_) -> Response:

    return Response(dumps({"api": "healthy"}))
