from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.project_name.apps.auth.exceptions import UserNotFound
from src.project_name.apps.auth.selectors import get_user_by_id
from src.project_name.config.jwt_settings import AuthJWT
from src.project_name.db.deps import get_db_session


async def require_user(
        db: AsyncSession = Depends(get_db_session),
        authorize: AuthJWT = Depends()
):
    try:
        authorize.jwt_required()
        user_id = authorize.get_jwt_subject()

        user = await get_user_by_id(db, user_id=int(user_id))

        if not user:
            raise UserNotFound('User no longer exist')

    except Exception as e:

        error = e.__class__.__name__

        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return user_id
