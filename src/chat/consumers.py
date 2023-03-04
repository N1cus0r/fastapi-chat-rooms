import json
from bson import json_util

from main import sio
from .models import Message


@sio.event
async def connect(sid, *args, **kwargs):
    print("CONNECTED")


@sio.event
async def join_room(sid, data):
    sio.enter_room(sid, data["code"])
    await sio.emit("join_room", room=data["code"])


@sio.event
async def leave_room(sid, data):
    if data["host_id"] == data["user_id"]:
        await sio.emit("host_left", room=data["code"])
    else:
        await sio.emit("user_left", room=data["code"])


@sio.event
async def chat_message(sid, data):
    message = await Message(
        text=data["text"],
        room_id=data["room_id"],
        user_id=data.get("user_id"),
        user_username=data.get("user_username"),
    ).insert()

    data["_id"] = str(message.id)
    data["time_sent"] = str(message.time_sent)

    await sio.emit("chat_message", data, room=data["room_code"])
