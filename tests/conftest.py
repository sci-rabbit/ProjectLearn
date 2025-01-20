import asyncio
import uuid
from datetime import timedelta

import pytest
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

import settings
from db.models import Base
from db.models import User
from db.session import get_async_session
from main import app
from settings import TEST_DATABASE_URL
from utils.security import create_access_token

# import asyncpg


test_engine = create_async_engine(TEST_DATABASE_URL)
test_session = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def setup_db():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture
async def async_client():
    async def override_get_async_session():
        async with test_session() as s:
            yield s

    app.dependency_overrides[get_async_session] = override_get_async_session

    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")


async def get_user_by_id(user_id: uuid.UUID):
    async with test_session() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        retrieved_data = result.scalar_one_or_none()

    return retrieved_data


async def get_users():
    async with test_session() as session:
        query = select(User)
        result = await session.execute(query)
        retrieved_data = result.scalars().all()

    return retrieved_data


def create_test_auth_headers_for_user(email: str):
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"Authorization": f"Bearer {access_token}"}
