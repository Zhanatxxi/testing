from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from src.project_name.config.jwt_settings import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from src.project_name.apps.auth.models import User
from src.project_name.apps.auth.schemas import UserCreateSchema, UserInDBSchema, SignInSchema, UserSignInSchema
from src.project_name.apps.auth.selectors import get_user_by_email
from src.project_name.apps.auth.services import signup, verify_password
from src.project_name.config.settings import settings
from src.project_name.db.deps import get_db_session

auth_route = APIRouter()


ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@auth_route.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInDBSchema
)
async def sign_up(
    user: UserCreateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    if await get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    user_ins = await signup(
        db,
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        surname=user.surname
    )

    return user_ins


@auth_route.post(
    "/sign-in",
    status_code=status.HTTP_200_OK,
    response_model=UserSignInSchema
)
async def sign_in(
    user_in: SignInSchema,
    authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db_session),
):
    user: User | None = await get_user_by_email(db, email=user_in.email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Incorrect Email or Password"
        )

    if not verify_password(user_in.password, user.hash_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect Email or Password"
        )

    access_token = authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    refresh_token = authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(days=REFRESH_TOKEN_EXPIRES_IN))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
