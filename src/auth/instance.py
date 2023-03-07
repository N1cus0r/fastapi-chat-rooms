from beanie import PydanticObjectId
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from .models import User
from .manager import get_user_manager

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy():
    return JWTStrategy(secret="SECRET", lifetime_seconds=3600)


backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [backend])

current_user = fastapi_users.current_user(active=True)
