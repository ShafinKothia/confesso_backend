import email
from typing import Optional, Union

from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class TokenData(BaseModel):
    email: Union[EmailStr, None] = None
    

