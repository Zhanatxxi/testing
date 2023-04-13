from datetime import date

from fastapi import APIRouter, Query, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.project_name.apps.analytic.schemas import AnalyticSchema
from src.project_name.apps.blog.selectors import get_count_like_blog
from src.project_name.apps.analytic.utils import get_analytic
from src.project_name.db.deps import get_db_session


analytic_route = APIRouter()


@analytic_route.get(
    "",
    response_model=list[AnalyticSchema | dict]
)
async def analytic(
    date_from: date = Query(default=date.today(), description="date from analytics like"),
    date_to: date = Query(default=date.today(), description="date to analytics like"),
    db: AsyncSession = Depends(get_db_session)
):
    analytic_response = await get_analytic(db)
    like_blogs_count = await get_count_like_blog(
        db,
        date_to=date_to,
        date_from=date_from
    )
    analytic_response.append(dict(likes=like_blogs_count))
    return analytic_response
