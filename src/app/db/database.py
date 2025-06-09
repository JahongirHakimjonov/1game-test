from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.app.core.settings import settings

assert settings.DATABASE_URL is not None, "DATABASE_URL не задан"
engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
