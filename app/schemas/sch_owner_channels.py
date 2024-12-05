from typing import Optional
from uuid import UUID
from pydantic import BaseModel


    # add schemas here

class SCH_Get_Owner_Channel_By_Id(BaseModel):
    id: UUID

class SCH_Get_Owner_Channels(BaseModel):
    skip: Optional[int]
