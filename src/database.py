from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import DB_URL

from auth.models import User
from rooms.models import Room
from chat.models import Message


async def init_mongodb():
    client = AsyncIOMotorClient(DB_URL)
    await init_beanie(database=client.chat, document_models=[User, Room, Message])
