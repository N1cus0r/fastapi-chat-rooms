import pytest
from typing import List
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_room(room: dict, room_host: dict):
    assert room["host_id"] == room_host["id"]

    assert room_host["id"] in room["participants_ids"]


@pytest.mark.anyio
async def test_join_and_leave_room(
    room: dict, other_users: List[dict], async_client: AsyncClient
):
    user_a, user_b = other_users

    user_a_join_response = await async_client.put(
        "/rooms/join-room",
        headers={"Authorization": f'Bearer {user_a["access_token"]}'},
        json={"code": room["code"]},
    )

    assert len(user_a_join_response.json()["participants_ids"]) == 2

    user_b_join_full_room_response = await async_client.put(
        "/rooms/join-room",
        headers={"Authorization": f'Bearer {user_b["access_token"]}'},
        json={"code": room["code"]},
    )

    assert user_b_join_full_room_response.status_code == 400

    assert user_b_join_full_room_response.json()["detail"] == "Room is full"

    user_b_leave_response = await async_client.put(
        "/rooms/leave-room",
        headers={"Authorization": f'Bearer {user_b["access_token"]}'},
        json={"code": room["code"]},
    )

    assert user_b_leave_response.status_code == 404

    assert user_b_leave_response.json()["detail"] == "User not in room"

    user_a_leave_response = await async_client.put(
        "/rooms/leave-room",
        headers={"Authorization": f'Bearer {user_a["access_token"]}'},
        json={"code": room["code"]},
    )

    user_a_leave_response_json = user_a_leave_response.json()

    assert user_a_leave_response.status_code == 200

    assert len(user_a_leave_response_json["participants_ids"]) == 1

    assert (
        user_a_leave_response_json["participants_ids"][0]
        == user_a_leave_response_json["host_id"]
    )

    user_b_join_room_response = await async_client.put(
        "/rooms/join-room",
        headers={"Authorization": f'Bearer {user_b["access_token"]}'},
        json={"code": room["code"]},
    )

    assert user_b_join_room_response.status_code == 200

    assert len(user_b_join_room_response.json()["participants_ids"]) == 2


@pytest.mark.anyio
async def test_get_room_messages(
    room: dict, room_host: dict, async_client: AsyncClient
):
    room_messages_response = await async_client.get(
        "/rooms/room-messages",
        headers={"Authorization": f'Bearer {room_host["access_token"]}'},
        params={"room_id": room["_id"]},
    )

    assert room_messages_response.status_code == 200

    assert len(room_messages_response.json()) == 10


@pytest.mark.anyio
async def test_get_updated_room_data(
    room: dict, room_host: dict, async_client: AsyncClient
):
    updated_room_response = await async_client.get(
        "/rooms/updated-room-data",
        headers={"Authorization": f'Bearer {room_host["access_token"]}'},
        params={"room_id": room["_id"]},
    )

    assert updated_room_response.status_code == 200

    assert len(updated_room_response.json()["messages"]) == 10

    assert updated_room_response.json()["room"]["_id"] == room["_id"]


@pytest.mark.anyio
async def test_user_in_room(other_users: List[dict], async_client: AsyncClient):
    user_b = other_users[1]
    
    user_b_in_room_response = await async_client.get(
        "/rooms/user-in-room",
        headers={"Authorization": f'Bearer {user_b["access_token"]}'},
    )

    assert user_b_in_room_response.status_code == 200

    assert user_b_in_room_response.json() is not None
    
