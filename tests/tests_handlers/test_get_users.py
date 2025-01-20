import pytest

from tests.conftest import get_users


@pytest.mark.asyncio
async def test_get_users(setup_db, async_client):
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

        resp = await aclient.get("/user/users")
        retrieved_data = await get_users()
        assert resp.status_code == 200
        assert resp.json() == [
            {
                "id": str(user.id),
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "password": user.password,
                "is_active": user.is_active,
            }
            for user in retrieved_data
        ]
