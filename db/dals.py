import uuid
from typing import List

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UserDAL:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_user(
        self, name: str, surname: str, email: EmailStr, password: str
    ) -> User:
        user_obj = User(name=name, surname=surname, email=email, password=password)
        self.db_session.add(user_obj)
        await self.db_session.flush()
        await self.db_session.commit()
        await self.db_session.refresh(user_obj)

        return user_obj

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        query = select(User).where(User.id == user_id)
        user_data = await self.db_session.execute(query)
        if user_data is not None:
            return user_data.scalar_one_or_none()

    async def get_users(self) -> List[User]:
        query = select(User)
        list_user_data = await self.db_session.execute(query)
        if list_user_data is not None:
            return list_user_data.scalars().all()

    async def update_user(self, user_id: uuid.UUID, **kwargs) -> User | None:
        query = update(User).where(User.id == user_id).values(kwargs).returning(User)
        res_user_data = await self.db_session.execute(query)
        await self.db_session.commit()
        return res_user_data.scalar_one_or_none()

    async def delete_user(self, user_id: uuid.UUID) -> User | None:
        query = (
            update(User)
            .where(User.id == user_id)
            .where(User.is_active == True)
            .values(is_active=False)
            .returning(User)
        )
        res_user_data = await self.db_session.execute(query)
        await self.db_session.commit()
        return res_user_data.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        user_data = await self.db_session.execute(query)
        if user_data is not None:
            return user_data.scalar_one_or_none()
