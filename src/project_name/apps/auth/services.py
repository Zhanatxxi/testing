from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from src.project_name.apps.auth.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def signup(
    db: AsyncSession,
    *,
    email: str,
    password: str,
    first_name: str | None,
    surname: str | None
):
    user = await create_user(
        db,
        email=email,
        password=password,
        first_name=first_name,
        surname=surname
    )
    return user


async def create_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
    first_name: str | None,
    surname: str | None
) -> User:
    hash_password = get_password_hash(password)
    user = User(
        email=email,
        hash_password=hash_password,
        first_name=first_name,
        surname=surname
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)

    return user
