import asyncio
import logging
from typing import Optional

from databases import Database, DatabaseURL
from src.repositories import _db_schema
from src.settings import Settings


async def run():
    settings = Settings()
    schema = _db_schema.metadata.schema

    db_url = DatabaseURL(settings.DATABASE_URL)
    assert db_url.username
    assert db_url.password

    async with Database(db_url.replace(database=db_url.database)) as db:
        await _create_schema(db, db_url.username, schema)


async def _create_schema(db: Database, username: str, schema: str):
    await db.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    await db.execute(f"GRANT USAGE ON SCHEMA {schema} TO {username}")
    await db.execute(
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA {schema} "
        f"GRANT SELECT, UPDATE ON SEQUENCES TO {username}"
    )
    await db.execute(
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA {schema} "
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {username}"
    )


if __name__ == "__main__":
    asyncio.run(run())

    print("Done")
