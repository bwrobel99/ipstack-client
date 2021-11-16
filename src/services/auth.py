from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from fastapi import HTTPException
from pydantic import BaseModel, Field
from src.domain.user import User
from src.helpers.dates import utcnow
from src.helpers.jwt import sign_jwt
from src.repositories import UserRepository

from ..helpers.hash import compare_password_with_hash, hash_password


class LoginInput(BaseModel):
    username: str
    password: str


class RegisterInput(BaseModel):
    username: str
    password: str
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


@dataclass(frozen=True)
class AuthService:
    user_repo: UserRepository

    async def login(self, raw_input: Dict[str, str]):
        validated_input = LoginInput(**raw_input)
        user = await self._authenticate(
            validated_input.username, validated_input.password
        )

        return {"access_token": sign_jwt(user.id)}

    async def register(self, raw_input: Dict[str, Any]) -> User:
        validated_input = RegisterInput(**raw_input)

        return await self.user_repo.create(
            {
                **validated_input.dict(exclude={"password"}),
                "password_hash": hash_password(validated_input.password),
            }
        )

    async def _authenticate(self, username: str, plain_password: str) -> User:
        user = await self.user_repo.get_by_username(username)

        if not user or not compare_password_with_hash(
            plain_password, user.password_hash
        ):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        return user
