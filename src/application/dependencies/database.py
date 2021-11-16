from databases import Database
from dependency_injector.resources import AsyncResource


class DatabaseResource(AsyncResource):
    async def init(self, db_url: str):
        db = Database(db_url)
        await db.connect()
        return db

    async def shutdown(self, db: Database):
        await db.disconnect()
