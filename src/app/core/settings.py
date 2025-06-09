import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "My Big Project")
    VERSION: str = os.getenv("VERSION", "1.0.0")


settings = Settings()
