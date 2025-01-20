from uuid import UUID

import pytest

from tests.conftest import get_user_by_id
from utils.hashing import Hasher


@pytest.mark.asyncio
async def test_handler_cu(setup_db, async_client):
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
    assert Hasher.verify_password(new_user["password"], resp.json()["password"]) is True

    retrieved_data = await get_user_by_id(UUID(resp.json()["id"]))

    assert retrieved_data.id == UUID(resp.json()["id"])
    assert retrieved_data.name == resp.json()["name"]
    assert retrieved_data.surname == resp.json()["surname"]
    assert retrieved_data.email == resp.json()["email"]
    assert retrieved_data.password == resp.json()["password"]
    assert retrieved_data.is_active == resp.json()["is_active"]


@pytest.mark.asyncio
async def test_handler_cu_with_same_email(setup_db, async_client):
    await setup_db

    new_user = {
        "name": "mini",
        "surname": "pekka",
        "email": "clashroyal@gmail.com",
        "password": "sosal?123",
    }

    new_user_with_same_email = {
        "name": "kurwa",
        "surname": "bob",
        "email": "clashroyal@gmail.com",
        "password": "fmkfmk223",
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

        retrieved_data = await get_user_by_id(UUID(resp.json()["id"]))

        assert retrieved_data.id == UUID(resp.json()["id"])
        assert retrieved_data.name == resp.json()["name"]
        assert retrieved_data.surname == resp.json()["surname"]
        assert retrieved_data.email == resp.json()["email"]
        assert retrieved_data.password == resp.json()["password"]
        assert retrieved_data.is_active == resp.json()["is_active"]

        resp = await aclient.post("/user/users", params=new_user_with_same_email)

        assert resp.status_code == 503


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_data_for_creation, expected_status_code",
    [
        ({}, 422),
        (
            {
                "name": "mi",
                "surname": "pekka",
                "email": "clashroyal@gmail.com",
                "password": "sosal?123",
            },
            422,
        ),
        (
            {
                "name": "mini",
                "surname": "pe",
                "email": "clashroyal@gmail.com",
                "password": "sosal?123",
            },
            422,
        ),
        (
            {
                "name": "123",
                "surname": "pekka",
                "email": "clashroyal@gmail.com",
                "password": "sosal?123",
            },
            422,
        ),
        (
            {
                "name": "mini",
                "surname": "123",
                "email": "clashroyal@gmail.com",
                "password": "sosal?123",
            },
            422,
        ),
        (
            {
                "name": "mini",
                "surname": "pekka",
                "email": "123",
                "password": "sosal?123",
            },
            422,
        ),
        (
            {
                "name": "mini",
                "surname": "pekka",
                "email": "clashroyal@gmail.com",
                "password": "sosal?1",
            },
            422,
        ),
        (
            {
                "name": "minifrjefrjkkfsdfkgjdkfgjkdfkgdjfkgkjdfjjgkdkfkgjdfjkgdjkkjd",
                "surname": "pekka",
                "email": "clashroyal@gmail.com",
                "password": "sosal?123",
            },
            422,
        ),
        (
            {
                "name": "mini",
                "surname": "pekkakdfgkefgjkdfkjgjkjkgfkgkfkgkdfgkf",
                "email": "clashroyal@gmail.com",
                "password": "sosal?123",
            },
            422,
        ),
        (
            {
                "name": "mini",
                "surname": "pekka",
                "email": "clashroyal@gmail.com",
                "password": "sosal?12kwejrrjwekfrkjfdjkgjkdfjkgfjkdgkdfhgfghjdfjhgdfhgjdfkhjghjkdfgjkdfjkgdjkgkdfgjdfgdk",
            },
            422,
        ),
        ({"name": "123", "surname": "123", "email": "123", "password": "123"}, 422),
    ],
)
async def test_validation_error(
    setup_db, async_client, user_data_for_creation, expected_status_code
):
    await setup_db

    aclient = await async_client
    async with aclient as aclient:
        resp = await aclient.post("/user/users", params=user_data_for_creation)

        assert resp.status_code == expected_status_code
