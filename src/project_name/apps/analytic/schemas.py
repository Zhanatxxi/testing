from datetime import datetime

from pydantic import BaseModel

from src.project_name.apps.blog.schemas import BlogInDBSchema


class AnalyticSchema(BaseModel):
    id: int
    email: str
    joined_date: datetime
    like_blogs: list[BlogInDBSchema]

    class Config:
        orm_mode = True