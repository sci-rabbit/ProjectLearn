import uuid
from uuid import UUID

import pytest

from tests.conftest import get_user_by_id


@pytest.mark.asyncio
async def test_get_user(setup_db, async_client):
    await setup_db

    new_user = {
        "name": "mini",
        "surname": "pekka",
        "email": "clashroyal@gmail.com",
        "password": "sosal?123",
    }

    aclient = await async_client
    async with aclient as aclient:
        resp = await aclient.post("/user/users", params=new_user)
        assert resp.status_code == 200
        assert resp.json()["name"] == new_user["name"]
        assert resp.json()["surname"] == new_user["surname"]
        assert resp.json()["email"] == new_user["email"]

        uuid_resp = resp.json()["id"]

        resp = await aclient.get(f"/user/users/{uuid_resp}")
        retrieved_data = await get_user_by_id(UUID(uuid_resp))

    assert resp.status_code == 200
    assert retrieved_data.id == UUID(resp.json()["id"])
    assert retrieved_data.name == resp.json()["name"]
    assert retrieved_data.surname == resp.json()["surname"]
    assert retrieved_data.email == resp.json()["email"]
    assert retrieved_data.password == resp.json()["password"]
    assert retrieved_data.is_active == resp.json()["is_active"]


@pytest.mark.asyncio
async def test_get_user_fake_uuid(setup_db, async_client):
    await setup_db

    user_id = uuid.uuid4()

    aclient = await async_client
    async with aclient as aclient:
        resp = await aclient.get(f"/user/users/{user_id}")

        assert resp.status_code == 404
