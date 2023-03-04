from fastapi.middleware.cors import CORSMiddleware

from src.config import CLIENT_HOST_URL
from src.main import app


origins = [
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT"],
    allow_headers=[
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
        "Content-Type",
        "Set-Cookie",
    ],
)
