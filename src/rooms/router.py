from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from beanie.odm.operators.update.array import Push, Pull
from beanie.operators import ElemMatch, In
from beanie import PydanticObjectId

from src.main import app
from src.auth.instance import current_user
from .schemas import UpdateRoom
from .models import Room
from src.auth.models import User
from src.chat.models import Message


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/create-room")
async def create_room(room_data: Room, user: User = Depends(current_user)):
    room = await Room.find_one(Room.host_id == user.id)

    if room:
        await room.update(
            {
                "$set": {
                    Room.max_participants: room_data.max_participants,
                    Room.participants_ids: [user.id],
                }
            }
        )
    else:
        room_data.host_id = user.id
        room_data.participants_ids = [user.id]
        room = await Room.insert_one(room_data)

    return room


@router.put("/join-room")
async def join_room(room_data: UpdateRoom, user: User = Depends(current_user)):
    room = await Room.find_one(Room.code == room_data.code)
    if room:
        if room.max_participants >= len(room.participants_ids):
            await room.update(Push({Room.participants_ids: user.id}))

            await Message(
                text=f"{user.username} joined the room", room_id=room.id
            ).insert()

            return room
        raise HTTPException(status_code=400, detail="Room is full")
    raise HTTPException(status_code=404, detail="Room does not exist")


@router.put("/leave-room")
async def leave_room(room_data: UpdateRoom, user: User = Depends(current_user)):
    room = await Room.find_one(Room.code == room_data.code)

    if room:
        if room.host_id == user.id:
            await Message.find(Message.room_id == room.id).delete()
            await room.delete()
            return JSONResponse(status_code=200, content={"message": "Room Deleted"})
        else:
            await room.update(Pull({Room.participants_ids: user.id}))

            await Message(
                text=f"{user.username} left the room", room_id=room.id
            ).insert()

            return room

    raise HTTPException(status_code=404, detail="Room does not exist")


@router.get("/room-messages")
async def get_room_messages(
    room_id: PydanticObjectId, user: User = Depends(current_user)
):
    messages = (
        await Message.find(Message.room_id == room_id)
        .sort("-time_sent")
        .limit(10)
        .to_list()
    )

    return messages


@router.get("/updated-room-data")
async def get_updated_room_data(
    room_id: PydanticObjectId, user: User = Depends(current_user)
):
    room = await Room.get(room_id)
    messages = (
        await Message.find(Message.room_id == room_id)
        .sort("-time_sent")
        .limit(10)
        .to_list()
    )

    return {"messages": messages, "room": room}


@router.get("/user-in-room")
async def check_if_user_in_room(user: User = Depends(current_user)):
    room = await Room.find(In(Room.participants_ids, [user.id])).first_or_none()
    return room


app.include_router(router)
