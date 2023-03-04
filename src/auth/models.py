from pydantic import EmailStr
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase


class User(BeanieBaseUser):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


async def get_user_db():
    yield BeanieUserDatabase(User)
