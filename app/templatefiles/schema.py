from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class SCH_Create_ReplaceTitle(BaseModel):
    id: UUID
    # add schemas here

class SCH_Get_ReplaceTitle_By_Id(BaseModel):
    id: UUID

class SCH_Get_ReplaceTitles(BaseModel):
    skip: Optional[int]