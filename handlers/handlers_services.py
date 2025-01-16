import uuid
from typing import List, Sequence

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from db.dals import UserDAL
from db.models import User
from pydantic_models.models import ShowUser, UserCreate


async def _create_user(body: UserCreate, session) -> ShowUser:
    user_dal_obj = UserDAL(session)
    try:
        new_user = await user_dal_obj.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            password=body.password
        )
    except IntegrityError:
        raise HTTPException(status_code=503, detail="User with same email already exist")

    return ShowUser(
        id=new_user.id,
        name=new_user.name,
        surname=new_user.surname,
        email=new_user.email,
        password=new_user.password,
        is_active=new_user.is_active
    )


async def _get_user_by_id(user_id: uuid.UUID, session) -> ShowUser:
    user_dal_obj = UserDAL(session)
    res_user = await user_dal_obj.get_user_by_id(user_id)
    if res_user is None:
        raise HTTPException(status_code=404, detail="User is not found")

    return ShowUser(
        id=res_user.id,
        name=res_user.name,
        surname=res_user.surname,
        email=res_user.email,
        password=res_user.password,
        is_active=res_user.is_active
    )


async def _get_users(session) -> List[ShowUser]:
    user_dal_obj = UserDAL(session)
    user_list = await user_dal_obj.get_users()

    if user_list is None:
        raise HTTPException(status_code=404, detail="Users are not found")

    return user_list


async def _update_user_by_id(user_id: uuid.UUID, body: dict, session) -> ShowUser:
    user_dal_obj = UserDAL(session)

    try:
        updated_user = await user_dal_obj.update_user(user_id, **body)
    except IntegrityError:
        raise HTTPException(status_code=503, detail="User with same email already exist")

    if updated_user is None:
        raise HTTPException(status_code=400, detail="Something went wrong")

    return ShowUser(
        id=updated_user.id,
        name=updated_user.name,
        surname=updated_user.surname,
        email=updated_user.email,
        password=updated_user.password,
        is_active=updated_user.is_active
    )


async def _delete_user_by_id(user_id: uuid.UUID, session):
    user_dal_obj = UserDAL(session)
    deleted_user = await user_dal_obj.delete_user(user_id)

    if deleted_user is None:
        raise HTTPException(status_code=400, detail="User already inactive")

    return ShowUser(
        id=deleted_user.id,
        name=deleted_user.name,
        surname=deleted_user.surname,
        email=deleted_user.email,
        password=deleted_user.password,
        is_active=deleted_user.is_active
    )
