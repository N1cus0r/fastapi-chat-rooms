from typing import Optional
from datetime import datetime
from pydantic import Field
from beanie import Document, PydanticObjectId


class Message(Document):
    text: str
    room_id: PydanticObjectId
    user_id: Optional[PydanticObjectId]
    user_username: Optional[str]
    time_sent: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "Message"
