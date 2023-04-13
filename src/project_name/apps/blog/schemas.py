from datetime import datetime

from pydantic import BaseModel, Field


class BlogSchema(BaseModel):
    title: str = Field(default=..., max_length=100, description="blog title")


class BlogCreateSchema(BlogSchema):
    pass


class BlogInDBSchema(BlogSchema):
    id: int
    author_id: int
    created_date: datetime
    updated_date: datetime | None
    
    class Config:
        orm_mode = True
