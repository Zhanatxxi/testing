from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from src.project_name.apps.blog.models import Blog, Like_Blog


async def insert_blog(
    db: AsyncSession,
    title: str,
    user_id: int
):
    blog = Blog(title=title, author_id=user_id)

    db.add(blog)
    await db.commit()
    await db.refresh(blog)
    return blog


async def insert_like_blog(
    db: AsyncSession,
    user_id: int,
    blog_id: int
):
    like = Like_Blog(
        user_id=user_id,
        blog_id=blog_id
    )
    db.add(like)
    await db.commit()


async def delete_like_blog(
        db: AsyncSession,
        user_id: int,
        blog_id: int
):
    like_blog = delete(Like_Blog)\
        .filter(Like_Blog.user_id == user_id) \
        .where(Like_Blog.blog_id == blog_id)

    await db.execute(like_blog)
    await db.commit()

