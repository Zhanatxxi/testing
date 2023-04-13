from sqlalchemy import (
    Column, Integer, String,
    DateTime, Boolean
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.project_name.db.base_model import Model


class User(Model):
    """SQLAlchemy declarative desc user table"""

    class Meta:
        verbose_name = "Пользователь"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=True, info={
        "verbose_name": "Имя пользователя"
    })
    surname = Column(String(100), nullable=True, info={
        "verbose_name": "Фамилия пользователя"
    })
    email = Column(String(length=255), unique=True, info={
        "verbose_name": "Email пользователя"
    })
    hash_password = Column(String(128), info={
        "verbose_name": "Password пользователя"
    })

    joined_date = Column(
        DateTime(timezone=True),
        server_default=func.now(), info={
            "verbose_name": "Дата когда пользователь зарег."
        })

    is_active = Column(Boolean(), default=False)

    like_blogs = relationship("Blog", secondary="like_blog")

    def __repr__(self):
        return f"id:{self.id} email: {self.email}"
