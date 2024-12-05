from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class SCH_Create_Channel(BaseModel):
    name: str
    images_allowed: bool

class SCH_Get_Channel_By_Id(BaseModel):
    id: UUID

class SCH_Join_Channel(BaseModel):
    quick_name: str

class SCH_Get_Channels(BaseModel):
    skip: Optional[int]
    limit: Optional[int]