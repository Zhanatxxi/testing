from pathlib import Path
from typing import Any

from pydantic import BaseSettings, validator, PostgresDsn


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = list(PostgresDsn.allowed_schemes) + ["postgresql+asyncpg"]


class Settings(BaseSettings):
    """Base settings project"""
    SECRET_KEY: str
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent
    APP_DIR = BASE_DIR / "src/project_name"
    DEBUG: bool

    CELERY_BROKER: str

    HOST_NAME: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 15
    SQLALCHEMY_DATABASE_URI: AsyncPostgresDsn | None = None

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    origins: list[str] = [
        "http://127.0.0.1:8000",
    ]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=f"/{values.get('DB_DATABASE') or ''}",
        )

    class Config:
        env_file = f"{Path(__file__).resolve().parent.parent}/.env"


settings = Settings()

