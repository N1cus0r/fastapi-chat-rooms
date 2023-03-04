from typing import Optional

from beanie import PydanticObjectId
from fastapi import Request, Depends
from fastapi_users.db import ObjectIDIDMixin, BeanieUserDatabase
from fastapi_users import BaseUserManager

from src.config import APP_SECRET
from .models import User, get_user_db


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = APP_SECRET
    verification_token_secret = APP_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
