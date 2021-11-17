from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    DATABASE_URL: str

    PASSWORD_HASH_SALT: str

    JWT_SECRET: str

    IPSTACK_API_KEY: str

    @validator("DATABASE_URL")
    def uri_to_sqlalchemy(cls, v: str) -> str:
        """
        The URI should start with postgresql://, not postgres://.
        SQLAlchemy used to accept both, but has removed support for the postgres name.
        """
        return v.replace("postgres://", "postgresql://")
