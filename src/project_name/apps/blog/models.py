from datetime import datetime

from sqlalchemy import (
    Column, Integer, String,
    DateTime, ForeignKey, Date
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.project_name.db.base_model import Model


class Like_Blog(Model):
    """SQLAlchemy declarative desc like blog many to many table"""
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    blog_id = Column(Integer, ForeignKey("blog.id"))
    create_date = Column(
        Date,
        default=datetime.now().date()
    )


class Blog(Model):
    """SQLAlchemy declarative desc blog table"""

    class Meta:
        verbose_name = "Blog"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

    created_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    like_users = relationship("User", secondary="like_blog", overlaps="like_blogs")

    def __repr__(self):
        return f"id:{self.id} email: {self.title}"
