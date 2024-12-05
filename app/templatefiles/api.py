'''Endpoints for Tables'''
from app.schemas.sch_ReplaceFileName import SCH_Create_ReplaceTitle, SCH_Get_ReplaceTitle_By_Id, SCH_Get_ReplaceTitles
from typing import Any, Optional
from app.crud.rep_ReplaceFileName import rep_ReplaceFileName
from pydantic.types import Json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ....schemas.sch_user import UserBase
from app.api import deps

router = APIRouter()

@router.get("/get_ReplaceLowercases")
def get_companies( data_in: SCH_Get_ReplaceTitles = Depends(), db_conn: Session = Depends(deps.get_db), ) -> Any:

    return rep_ReplaceFileName.get_ReplaceLowercases(db=db_conn, data_in=data_in)

@router.get("/get_ReplaceLowercase_by_id")
def get_companies(data_in: SCH_Get_ReplaceTitle_By_Id = Depends(), db_conn: Session = Depends(deps.get_db)) -> Any:
    
    return rep_ReplaceFileName.get_ReplaceLowercase_by_id(db=db_conn, data_in=data_in)

# @router.post("/get_company_by_id")
# def get_companybyid(company_id: SCH_Get_Company_By_Id ,db_conn: Session = Depends(deps.get_db)) -> Any:

#     return rep_companies.get_company_by_id( company_id=company_id.id  , db=db_conn )

@router.post("/create_ReplaceLowercase")
def create_button(data_in: SCH_Create_ReplaceTitle , db_conn: Session = Depends(deps.get_db), current_user: UserBase = Depends(deps.get_current_active_user) ) -> Any:
    res = rep_ReplaceFileName.create_ReplaceLowercase(data_in=data_in, db=db_conn)
    if res == "Done":
        return res
