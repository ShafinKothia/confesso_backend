from fastapi import UploadFile, File
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class SCH_Create_Confession(BaseModel):
    confession: Optional[str]
    channel_id: UUID

class SCH_Get_Confession_By_Id(BaseModel):
    id: UUID

class SCH_Get_Confessions(BaseModel):
    skip: Optional[int]
    limit: Optional[int]

class SCH_Get_Confession_Pages(BaseModel):
    limit: Optional[int]

class SCH_Get_Confession_Pages_By_Channel_Id(BaseModel):
    limit: int
    channel_id: UUID

class SCH_Get_Unapproved_Confessions(BaseModel):
    limit: Optional[int]
    skip: Optional[int]
    channel_id: UUID

class SCH_Get_Confessions_By_Channel_Id(BaseModel):
    skip: Optional[int]
    limit: Optional[int]
    channel_id: UUID