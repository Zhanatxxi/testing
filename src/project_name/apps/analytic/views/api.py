from datetime import date

from fastapi import APIRouter, Query, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.project_name.db.deps import get_db_session

from src.project_name.apps.blog.selectors import get_count_like_blog


analytic_route = APIRouter()


@analytic_route.get("")
async def analytic(
    date_from: date = Query(default=date.today(), description="date from analytics like"),
    date_to: date = Query(default=date.today(), description="date to analytics like"),
    db: AsyncSession = Depends(get_db_session)
):
    like_blogs_count = await get_count_like_blog(db, date_to=date_to, date_from=date_from)
    return like_blogs_count
