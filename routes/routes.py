import uuid
from typing import Annotated
from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.session import get_async_session
from handlers.handlers_services import _create_user
from handlers.handlers_services import _delete_user_by_id
from handlers.handlers_services import _get_user_by_id
from handlers.handlers_services import _get_users
from handlers.handlers_services import _update_user_by_id
from handlers.login_handlers import get_current_user_from_token
from pydantic_models.models import ShowUser
from pydantic_models.models import UpdateUserRequest
from pydantic_models.models import UserCreate

user_router = APIRouter()


@user_router.post("/users")
async def create_user(
    user_data: Annotated[UserCreate, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ShowUser:
    return await _create_user(user_data, session)


@user_router.get("/users/{user_id}")
async def get_user(
    user_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_async_session)]
) -> ShowUser:
    return await _get_user_by_id(user_id, session)


@user_router.get("/users")
async def get_users(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> List[ShowUser]:
    return await _get_users(session)


@user_router.put("/users/{user_id}")
async def update_user(
    user_id: uuid.UUID,
    body: Annotated[UpdateUserRequest, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user_from_token)],
) -> ShowUser:
    data_req = body.model_dump(exclude_none=True)

    if data_req == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )

    await _get_user_by_id(user_id, session)
    return await _update_user_by_id(user_id, data_req, session)


@user_router.delete("/users/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(get_current_user_from_token)],
) -> ShowUser:
    await _get_user_by_id(user_id, session)

    return await _delete_user_by_id(user_id, session)
