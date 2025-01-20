from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from db.dals import UserDAL
from db.models import User
from db.session import get_async_session
from utils.hashing import Hasher


async def _get_user_by_email_for_auth(email, session) -> User | None:
    user_dal_obj = UserDAL(session)
    return await user_dal_obj.get_user_by_email(email=email)


async def authenticate_user(email: str, password: str, session) -> User | None:
    user = await _get_user_by_email_for_auth(email, session)
    if user is None:
        return
    if not Hasher.verify_password(password, user.password):
        return
    return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def get_current_user_from_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            print(username)
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await _get_user_by_email_for_auth(username, session)
    if user is None:
        raise credentials_exception

    return user
