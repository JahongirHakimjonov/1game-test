from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from src.app.core.settings import settings
from src.app.db.database import engine
from src.app.db.models.tournament import Base


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def setup() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

    @app.on_event("startup")
    async def on_startup():
        await create_tables(engine)

    return app
