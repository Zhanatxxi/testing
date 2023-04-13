from typing import Generator

from src.project_name.db.session import Session


async def get_db_session() -> Generator:
    async with Session() as session:
        yield session
