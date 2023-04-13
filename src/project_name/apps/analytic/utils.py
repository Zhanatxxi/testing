import sqlalchemy.ext.asyncio

from src.project_name.apps.auth.selectors import get_users_with_like_blogs


async def get_analytic(
    db: sqlalchemy.ext.asyncio.AsyncSession,
):
    """ select count like blog filter date """

    users = await get_users_with_like_blogs(db)
    return users
