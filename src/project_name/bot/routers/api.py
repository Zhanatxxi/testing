from fastapi import APIRouter

from src.project_name.bot.apps.create_user.views.api import bot_router


api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(bot_router, prefix="/create_user", tags=["Create User"])
