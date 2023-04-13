from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.project_name.bot.main import bot_app
from src.project_name.config.settings import settings
from src.project_name.routers.api import api_v1


app = FastAPI(
    title="Testing project",
    description="This's service for testing project",
    debug=settings.DEBUG
)


app.mount(path="/bot", app=bot_app)


app.include_router(api_v1)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


