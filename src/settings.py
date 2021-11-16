from pydantic import BaseSettings


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
