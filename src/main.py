from fastapi import FastAPI
from socketio import AsyncServer, ASGIApp, AsyncRedisManager

from src.database import init_mongodb
from src.config import REDIS_HOST_URL

app = FastAPI()

import src.cors

from src.auth import router
from src.rooms import router

redis_manager = AsyncRedisManager(url=REDIS_HOST_URL, write_only=False)
sio = AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=src.cors.origins,
    client_manager=redis_manager,
)
socket_app = ASGIApp(sio)
app.mount("/", socket_app)

import src.chat.consumers


@app.on_event("startup")
async def connect_db():
    await init_mongodb()
