import uuid
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from db.session import get_async_session
from handlers.handlers_services import _create_user, _get_user_by_id, _get_users, _update_user_by_id, _delete_user_by_id
from pydantic_models.models import UserCreate, ShowUser, UpdateUserRequest

user_router = APIRouter()


@user_router.post("/users")
async def create_user(user_data: Annotated[UserCreate, Depends()],
                      session: Annotated[AsyncSession, Depends(get_async_session)],
                      ) -> ShowUser:
    return await _create_user(user_data, session)


@user_router.get("/users/{user_id}")
async def get_user(user_id: uuid.UUID,
                   session: Annotated[AsyncSession, Depends(get_async_session)]) -> ShowUser:
    return await _get_user_by_id(user_id, session)


@user_router.get("/users")
async def get_users(session: Annotated[AsyncSession, Depends(get_async_session)]) -> List[ShowUser]:
    return await _get_users(session)


@user_router.put("/users/{user_id}")
async def update_user(user_id: uuid.UUID, body: Annotated[UpdateUserRequest, Depends()],
                      session: Annotated[AsyncSession, Depends(get_async_session)]) -> ShowUser:
    data_req = body.model_dump(exclude_none=True)

    if data_req == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")

    await _get_user_by_id(user_id, session)
    return await _update_user_by_id(user_id, data_req, session)


@user_router.delete("/users/{user_id}")
async def delete_user(user_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_async_session)]) -> ShowUser:
    await _get_user_by_id(user_id, session)

    return await _delete_user_by_id(user_id, session)

