from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import DB_URL, TEST_DB_URL

from src.auth.models import User
from src.rooms.models import Room
from src.chat.models import Message


async def init_mongodb():
    client = AsyncIOMotorClient(DB_URL)
    await init_beanie(database=client.chat, document_models=[User, Room, Message])


async def init_test_mongodb():
    client = AsyncIOMotorClient(TEST_DB_URL)
    await init_beanie(database=client.chat, document_models=[User, Room, Message])
