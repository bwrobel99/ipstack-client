from contextlib import contextmanager
from dataclasses import dataclass

from fastapi import HTTPException
from pydantic import ValidationError as PydanticValidationError


@dataclass
class ValidationError(HTTPException):
    status_code: int = 400
    detail: str = "Validation Error"


@dataclass
class DatabaseError(HTTPException):
    status_code: int = 500
    detail: str = "Database Error"


class HttpClientError(HTTPException):
    def __init__(
        self,
        ipstack_message: str,
    ) -> None:
        super().__init__(500, detail=f"IPStack API Error: {ipstack_message}")


@contextmanager
def map_pydantic_errors_to_http():
    try:
        yield
    except PydanticValidationError:
        raise ValidationError()
