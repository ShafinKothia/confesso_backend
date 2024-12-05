'''config settings'''
from uuid import UUID
from pydantic import BaseModel


class SCMCompanyBase(BaseModel):
    '''config settings'''
    id: UUID

class SCMCompanyPrefix(BaseModel):
    '''config settings'''
    id: UUID
    prefix: str

class SCMCompanyList(SCMCompanyBase):
    '''config settings'''
    name: str
    prefix: str


    class Config:
        '''config settings'''
        orm_mode = True

