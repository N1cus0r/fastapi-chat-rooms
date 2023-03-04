from typing import Optional, List
from pydantic import BaseModel
from beanie import PydanticObjectId


class UpdateRoom(BaseModel):
    code: Optional[str]
    max_participants: Optional[int]
    host_id: Optional[PydanticObjectId]
    participants_ids: Optional[List[PydanticObjectId]]
