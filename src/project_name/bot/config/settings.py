from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    URL: str

    class Config:
        env_file = f"{Path(__file__).resolve().parent.parent}/.env"


settings = Settings()
