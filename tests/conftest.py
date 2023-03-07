import pytest
from random import randint
from typing import List
from httpx import AsyncClient
from faker import Faker

from src.main import app
from src.database import init_test_mongodb
from src.auth.models import User
from src.rooms.models import Room
from src.chat.models import Message


fake = Faker()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def connect_and_clear_db():
    await init_test_mongodb()
    yield
    await User.find().delete()
    await Room.find().delete()
    await Message.find().delete()


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_users(async_client: AsyncClient) -> List[dict]:
    users = []
    for _ in range(3):
        create_user_response = await async_client.post(
            "/auth/register",
            json={
                "username": fake.name(),
                "email": fake.email(),
                "password": "password",
            },
        )

        user_json = create_user_response.json()

        access_token_response = await async_client.post(
            "/auth/jwt/login",
            data={"username": user_json["email"], "password": "password"},
        )

        token_json = access_token_response.json()

        user_json["access_token"] = token_json["access_token"]

        users.append(user_json)

    return users


@pytest.fixture(scope="session")
async def room_host(authenticated_users):
    return authenticated_users[0]


@pytest.fixture(scope="session")
async def other_users(authenticated_users):
    return authenticated_users[1::]


@pytest.fixture(scope="session")
async def room(room_host, async_client):
    response = await async_client.post(
        "/rooms/create-room",
        headers={"Authorization": f"Bearer {room_host['access_token']}"},
        json={"max_participants": 2},
    )

    for _ in range(11):
        await Message(
            text=fake.sentence(),
            room_id=response.json()["_id"],
            user_id=room_host["id"],
            user_username=room_host["username"],
        ).insert()

    return response.json()
