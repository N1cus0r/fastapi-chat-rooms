from beanie import PydanticObjectId
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    JWTStrategy,
    CookieTransport,
)

from config import DEBUG
from .models import User
from .manager import get_user_manager

cookie_transport = CookieTransport(
    cookie_name="mayaLoh",
    cookie_httponly=False,
    cookie_secure=True if DEBUG == "False" else False,
    cookie_samesite="none" if DEBUG == "False" else "lax",
    cookie_max_age=3600,
)


def get_jwt_strategy():
    return JWTStrategy(secret="SECRET", lifetime_seconds=3600)


backend = AuthenticationBackend(
    name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [backend])

current_user = fastapi_users.current_user(active=True)
