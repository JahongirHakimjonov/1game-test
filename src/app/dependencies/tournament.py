from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.app.core.settings import settings

assert settings.DATABASE_URL is not None, "DATABASE_URL не задан"
engine_test = create_async_engine(settings.DATABASE_URL, echo=True)
async_session_test = async_sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session:
        yield session
