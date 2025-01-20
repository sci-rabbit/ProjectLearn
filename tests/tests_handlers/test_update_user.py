from uuid import UUID

import pytest

from tests.conftest import get_user_by_id


@pytest.mark.asyncio
async def test_update_user(setup_db, async_client):
    await setup_db

    new_user = {
        "name": "mini",
        "surname": "pekka",
        "email": "clashroyal@gmail.com",
        "password": "sosal?123",
    }

    update_data = {"name": "MINI", "surname": "PEKKA", "password": "SOSAL?123"}

    aclient = await async_client
    async with aclient as aclient:
        resp = await aclient.post("/user/users", params=new_user)
        assert resp.status_code == 200
        assert resp.json()["name"] == new_user["name"]
        assert resp.json()["surname"] == new_user["surname"]
        assert resp.json()["email"] == new_user["email"]

        uuid_resp = resp.json()["id"]

        resp = await aclient.put(f"/user/users/{uuid_resp}", params=update_data)
        retrieved_data = await get_user_by_id(UUID(uuid_resp))

    assert retrieved_data.id == UUID(resp.json()["id"])
    assert retrieved_data.name == resp.json()["name"]
    assert retrieved_data.surname == resp.json()["surname"]
    assert retrieved_data.email == resp.json()["email"]
    assert retrieved_data.password == resp.json()["password"]
    assert retrieved_data.is_active == resp.json()["is_active"]

    assert retrieved_data.name == update_data["name"]
    assert retrieved_data.surname == update_data["surname"]


@pytest.mark.asyncio
async def test_update_user_with_same_email(setup_db, async_client):
    await setup_db

    new_user = {
        "name": "mini",
        "surname": "pekka",
        "email": "clashroyal@gmail.com",
        "password": "sosal?123",
    }

    new_user2 = {
        "name": "bob",
        "surname": "kenny",
        "email": "penis@gmail.com",
        "password": "dsfmskd342234",
    }

    update_data = {"email": "clashroyal@gmail.com"}

    aclient = await async_client
    async with aclient as aclient:
        await aclient.post("/user/users", params=new_user)
        resp_post2 = await aclient.post("/user/users", params=new_user2)

        uuid_resp = resp_post2.json()["id"]

        resp_put = await aclient.put(f"/user/users/{uuid_resp}", params=update_data)

    assert resp_put.status_code == 503


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_data_for_update, expected_status_code",
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
async def test_update_validation_error(
    setup_db, async_client, user_data_for_update, expected_status_code
):
    await setup_db

    new_user = {
        "name": "mini",
        "surname": "pekka",
        "email": "clashroyal@gmail.com",
        "password": "sosal?123",
    }

    aclient = await async_client
    async with aclient as aclient:
        resp_post = await aclient.post("/user/users", params=new_user)

        uuid_resp = resp_post.json()["id"]

        resp_put = await aclient.put(
            f"/user/users/{uuid_resp}", params=user_data_for_update
        )

        assert resp_put.status_code == expected_status_code
