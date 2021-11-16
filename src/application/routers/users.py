from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.application.dependencies import Container
from src.services import AuthService

auth_router = APIRouter()


@auth_router.post("/auth/login")
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_svc: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_svc.login(
        {"username": form_data.username, "password": form_data.password}
    )


@auth_router.post("/auth/register")
@inject
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_svc: AuthService = Depends(Provide[Container.auth_service]),
):
    user = await auth_svc.register(
        {"username": form_data.username, "password": form_data.password}
    )
    return user.dict(exclude={"password_hash"})
