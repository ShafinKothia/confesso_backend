from datetime import datetime, timedelta
import random
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, UploadFile, File
from sqlalchemy.orm.session import Session
from .auth import AuthHandler
from app.schemas.sch_confessions import SCH_Create_Confession, SCH_Get_Unapproved_Confessions, SCH_Get_Confession_By_Id, SCH_Get_Confessions, SCH_Get_Confession_Pages, SCH_Get_Confessions_By_Channel_Id, SCH_Get_Confession_Pages_By_Channel_Id
from app.schemas.sch_user import UserMe
from app.api import deps
from app.core import security
from app.crud import rep_confessions
from app.crud.rep_joined_channels import rep_joined_channels
from fastapi.responses import HTMLResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig, MessageType
import json
from app.core.config import settings
from uuid import UUID


router = APIRouter()

auth_handler = AuthHandler()

# to get a string like this run:
# openssl rand -hex 32



# @router.get("/get_all_confessions")
# async def get_channels(data_in: SCH_Get_Confessions = Depends(), db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
#     if current_user.username == "anonymous":
#         return rep_confessions.get_confessions(db=db_conn, data_in=data_in)
#     else:
#         raise HTTPException(
#             status_code=401,
#             detail="Not Authorized"
#         )


@router.post('/create_confession_image/{confession_id}')
async def create_channel(confession_id: UUID, image_in: UploadFile = File(...), db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    # print(image_in.filename)
    return await rep_confessions.add_image(db=db_conn, image_file=image_in, confession_id=confession_id)

@router.get('/get_confession_image')
async def create_channel(image_path: SCH_Get_Confession_By_Id = Depends(),  db_conn: Session = Depends(deps.get_db)):
    return rep_confessions.get_image(db=db_conn, image_id=image_path.id)

@router.post('/create_confession')
async def create_channel(  confession_in: SCH_Create_Confession, db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    is_joined_channel = rep_joined_channels.is_joined_channel(db=db_conn, user_id=current_user.id, channel_id=confession_in.channel_id)
    if not is_joined_channel:
        raise HTTPException(
            status_code=401,
            detail="Not Joined Channel"
        )
    return rep_confessions.create_confession(db=db_conn, confession_in=confession_in)

@router.get("/get_confession_by_id")
async def get_channel_by_id(data_in: SCH_Get_Confession_By_Id = Depends(), db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    return rep_confessions.get_confession_by_id(db=db_conn, confession_id=data_in.id)

@router.get("/get_confessions_by_channel_id")
async def get_channel_by_id(data_in: SCH_Get_Confessions_By_Channel_Id = Depends(), db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    is_joined_channel = rep_joined_channels.is_joined_channel(db=db_conn, user_id=current_user.id, channel_id=data_in.channel_id)
    if not is_joined_channel:
        raise HTTPException(
            status_code=401,
            detail="Not Joined Channel"
        )
        
    return rep_confessions.get_confessions_by_channel_id(db=db_conn, data_in=data_in)

@router.get("/get_no_of_confession_pages")
async def get_channel_by_id(data_in: SCH_Get_Confession_Pages = Depends(), db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    return rep_confessions.get_no_of_confession_pages(db=db_conn, data_in=data_in)

@router.get("/get_no_of_confession_pages_by_channel_id")
async def get_channel_by_id(data_in: SCH_Get_Confession_Pages_By_Channel_Id = Depends(), db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    return rep_confessions.get_no_of_confession_pages_by_channel_id(db=db_conn, data_in=data_in)

@router.get("/get_unapproved_confessions")
async def get_channel_by_id(data_in: SCH_Get_Unapproved_Confessions = Depends(), db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    return rep_confessions.get_unapproved_confessions(db=db_conn, data_in=data_in, user_id  = current_user.id)

@router.post("/approve_confession")
async def get_channel_by_id(data_in: SCH_Get_Confession_By_Id , db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    return rep_confessions.approve_confession(db=db_conn, confession_id=data_in.id)
    

