from fastapi import APIRouter

from src.project_name.apps.analytic.views.api import analytic_route
from src.project_name.apps.auth.views.api import auth_route
from src.project_name.apps.blog.views.api import blog_router

api_v1 = APIRouter(prefix="/api/v1")


api_v1.include_router(auth_route, prefix="/auth", tags=["User"])
api_v1.include_router(blog_router, prefix="/blog", tags=["Blog"])
api_v1.include_router(analytic_route, prefix="/analytic", tags=["Analytic"])
