from random import choices
from string import ascii_uppercase
from typing import List, Optional

from pydantic import Field, ValidationError, validator
from beanie import Document, PydanticObjectId


def generate_room_code():
    return "".join(choices(ascii_uppercase, k=6))


class Room(Document):
    code: str = Field(default_factory=generate_room_code)
    max_participants: int
    host_id: Optional[PydanticObjectId]
    participants_ids: Optional[List[PydanticObjectId]]

    class Settings:
        name = "Room"

    @validator("max_participants")
    def validate_max_participants(cls, value):
        if not (2 <= value <= 5):
            raise ValidationError("max_participant should be in range of 2-5")

        return value
