from fastapi import FastAPI

from src.project_name.bot.routers.api import api_v1

bot_app: FastAPI = FastAPI(
    title="Bot Automation",
    description="Automation create user"
)


bot_app.include_router(api_v1)
