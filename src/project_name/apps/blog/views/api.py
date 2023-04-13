from fastapi import APIRouter, HTTPException, Depends, status, Path

from src.project_name.apps.auth.deps import require_user
from src.project_name.apps.blog.schemas import BlogCreateSchema, BlogInDBSchema
from src.project_name.apps.blog.selectors import select_blogs, get_blog_by_id, get_like_on_blog
from src.project_name.apps.blog.services import insert_blog, insert_like_blog, delete_like_blog
from sqlalchemy.ext.asyncio import AsyncSession

from src.project_name.db.deps import get_db_session


blog_router = APIRouter()


@blog_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BlogInDBSchema
)
async def create_blog(
    blog: BlogCreateSchema,
    user_id: str = Depends(require_user),
    db: AsyncSession = Depends(get_db_session)
):
    blog = await insert_blog(db, title=blog.title, user_id=int(user_id))
    return blog


@blog_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[BlogInDBSchema],
)
async def get_blogs(
    db: AsyncSession = Depends(get_db_session)
):
    blogs = await select_blogs(db)
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Not blogs"
        )

    return blogs


@blog_router.post("/{blog_id}")
async def blog_like(
    blog_id: int = Path(gt=0, description="blog id"),
    db: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(require_user)
):
    blog = await get_blog_by_id(db, blog_id=blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found!!!"
        )

    if await get_like_on_blog(db, blog_id=blog_id, user_id=int(user_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are liked it's blog!!!"
        )

    await insert_like_blog(
        db,
        user_id=int(user_id),
        blog_id=blog_id
    )

    return "Like on blog"


@blog_router.delete("/{blog_id}")
async def blog_unlike(
    blog_id: int = Path(gt=0, description="blog id"),
    db: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(require_user)
):
    blog = await get_blog_by_id(db, blog_id=blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found!!!"
        )

    await delete_like_blog(
        db,
        user_id=int(user_id),
        blog_id=blog_id
    )

    return "Unlike on blog"
