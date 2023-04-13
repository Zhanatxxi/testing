from pydantic import BaseModel, Field, EmailStr
from pydantic import validator

from src.project_name.apps.auth.exceptions import PasswordError


class UserSchema(BaseModel):
    email: EmailStr = Field(default=..., description="user email")
    first_name: str | None = Field(default=None, description="user name")
    surname: str | None = Field(default=None, description="user suranme")


class UserCreateSchema(UserSchema):
    password: str = Field(default=..., min_length=8, description="password")
    password_confirm: str = Field(default=..., min_length=8, description="password_confirm")

    @validator("password_confirm")
    def password_confirm_validate(cls, v, values, **kwargs):
        if v != values.get("password"):
            raise PasswordError("Password not equal")
        return v


class UserInDBSchema(UserSchema):
    id: int
    hash_password: str

    class Config:
        orm_mode = True


class SignInSchema(BaseModel):
    email: EmailStr = Field(default=..., description="user email")
    password: str = Field(default=..., min_length=8, description="password")


class UserSignInSchema(BaseModel):
    access_token: str = Field(default=..., description="access_token")
    refresh_token: str = Field(default=..., description="refresh_token")
