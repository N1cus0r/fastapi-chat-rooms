from typing import Optional

from pydantic import EmailStr
from beanie import PydanticObjectId
from fastapi_users import schemas


class UserRead(schemas.BaseUser[PydanticObjectId]):
    id: PydanticObjectId
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
