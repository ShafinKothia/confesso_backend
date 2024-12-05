from lib2to3.pytree import Base
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr



class UserMe(BaseModel): 
    username: str
    id: UUID
    class Config:
        orm_mode = True
    


# Properties to receive via API on creation
class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str







