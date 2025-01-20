import uuid
from uuid import UUID

import pytest

from tests.conftest import create_test_auth_headers_for_user
from tests.conftest import get_user_by_id
from utils.hashing import Hasher


@pytest.mark.asyncio
async def test_delete_user(setup_db, async_client):
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
        assert (
            Hasher.verify_password(new_user["password"], resp.json()["password"])
            is True
        )

        uuid_resp = resp.json()["id"]

        resp = await aclient.delete(
            f"/user/users/{uuid_resp}",
            headers=create_test_auth_headers_for_user(new_user["email"]),
        )

    retrieved_data = await get_user_by_id(UUID(uuid_resp))

    assert resp.status_code == 200
    assert retrieved_data.id == UUID(resp.json()["id"])
    assert retrieved_data.name == resp.json()["name"]
    assert retrieved_data.surname == resp.json()["surname"]
    assert retrieved_data.email == resp.json()["email"]
    assert retrieved_data.password == resp.json()["password"]
    assert retrieved_data.is_active is False


@pytest.mark.asyncio
async def test_delete_user_fake_uuid(setup_db, async_client):
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
        assert (
            Hasher.verify_password(new_user["password"], resp.json()["password"])
            is True
        )

        user_id = uuid.uuid4()

        resp = await aclient.delete(
            f"/user/users/{user_id}",
            headers=create_test_auth_headers_for_user(new_user["email"]),
        )

        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_bad_cred(setup_db, async_client):
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
        assert (
            Hasher.verify_password(new_user["password"], resp.json()["password"])
            is True
        )

        uuid_resp = uuid.uuid4()

        resp = await aclient.delete(
            f"/user/users/{uuid_resp}",
            headers=create_test_auth_headers_for_user(new_user["email"] + "a1213"),
        )

        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_delete_user_unauth(setup_db, async_client):
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
        assert (
            Hasher.verify_password(new_user["password"], resp.json()["password"])
            is True
        )
        bad_auth_headers = create_test_auth_headers_for_user(new_user["email"])
        bad_auth_headers["Authorization"] += "a"

        uuid_resp = resp.json()["id"]

        resp = await aclient.delete(
            f"/user/users/{uuid_resp}",
            headers=bad_auth_headers,
        )

        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_delete_user_no_token(setup_db, async_client):
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
        assert (
            Hasher.verify_password(new_user["password"], resp.json()["password"])
            is True
        )
        uuid_resp = resp.json()["id"]
        resp = await aclient.delete(
            f"/user/users/{uuid_resp}",
        )

        assert resp.status_code == 401
