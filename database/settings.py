import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Used cars scraper API"

    DATABASE_URL: str | None = (
        f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
