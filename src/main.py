from fastapi import FastAPI
from socketio import AsyncServer, ASGIApp, AsyncRedisManager 


from database import init_mongodb
from config import REDIS_HOST_URL


app = FastAPI()

import cors

from auth import router
from rooms import router


redis_manager = AsyncRedisManager(url=REDIS_HOST_URL, write_only=False)
sio = AsyncServer(
    async_mode="asgi", cors_allowed_origins=cors.origins,
    client_manager=redis_manager
)
socket_app = ASGIApp(sio)
app.mount("/", socket_app)


import chat.consumers


@app.on_event("startup")
async def connect_db():
    await init_mongodb()
