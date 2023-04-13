from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.project_name.apps.auth.models import User


async def get_user_by_email(db: AsyncSession, *, email: str) -> User | None:
    stmt = select(User).where(User.email.like("%{}%".format(email)))
    result = await db.scalar(stmt)
    return result


async def get_user_by_id(db: AsyncSession, *, user_id: int):
    stmt = select(User) \
            .where(User.id == user_id)
    user = await db.scalar(stmt)
    return user

