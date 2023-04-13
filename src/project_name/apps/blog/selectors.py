import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from src.project_name.apps.blog.models import Blog, Like_Blog


async def select_blogs(db: AsyncSession) -> list[Blog | None]:
    """ get all blogs """
    stmt = select(Blog)
    blogs = await db.scalars(stmt)
    return blogs.all()


async def get_blog_by_id(db: AsyncSession, *, blog_id: int) -> Blog | None:
    """ get blog where blog.id == blog_id """
    stmt = select(Blog).where(Blog.id == blog_id)
    blog = await db.scalar(stmt)
    return blog


async def get_like_on_blog(db: AsyncSession, *, user_id: int, blog_id: int):
    stmt = select(Like_Blog.id)\
        .filter(Like_Blog.user_id == user_id)\
        .where(Like_Blog.blog_id == blog_id)\

    like = await db.scalar(stmt)
    return like


async def get_count_like_blog(
        db: AsyncSession,
        *,
        date_from: datetime.date = datetime.date.today(),
        date_to: datetime.date = datetime.date.today()
):
    """ select count like blog filter date """
    stmt = select(func.count(Like_Blog.id))\
        .filter(
        and_(
            Like_Blog.create_date >= date_from,
            Like_Blog.create_date <= date_to
            )
        )
    like_blogs_count = await db.scalar(stmt)
    return like_blogs_count
