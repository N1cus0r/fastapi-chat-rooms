from src.main import app
from .instance import fastapi_users, backend
from .schemas import UserRead, UserCreate, UserUpdate


app.include_router(
    fastapi_users.get_auth_router(backend), prefix="/auth/jwt", tags=["Auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)
