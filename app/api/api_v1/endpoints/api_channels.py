from datetime import datetime, timedelta
import random
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm.session import Session
from .auth import AuthHandler
from app.schemas.sch_channels import SCH_Get_Channels, SCH_Get_Channel_By_Id, SCH_Create_Channel, SCH_Join_Channel
from app.schemas.sch_user import UserMe
from app.api import deps
from app.core import security
from app.crud import rep_channels
from fastapi.responses import HTMLResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig, MessageType
import json
from app.core.config import settings



router = APIRouter()

auth_handler = AuthHandler()

# to get a string like this run:
# openssl rand -hex 32



@router.get("/get_channels")
async def get_channels(data_in: SCH_Get_Channels = Depends(), db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    if current_user.username == "anonymous":
        return rep_channels.get_channels(db=db_conn, data_in=data_in)
    else:
        raise HTTPException(
            status_code=401,
            detail="Not Authorized"
        )

@router.post('/create_channel')
async def create_channel(  channel_in: SCH_Create_Channel, db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    
    return rep_channels.create_channel(db=db_conn, channel_in=channel_in, user_id=current_user.id)
   
@router.get("/get_channel_by_id")
async def get_channel_by_id(data_in: SCH_Get_Channel_By_Id = Depends(), db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    return rep_channels.get_channel_by_id(db=db_conn, channel_id=data_in.id)

@router.get("/get_self_channels")
async def get_channel_by_id(db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    return rep_channels.get_self_channels(db=db_conn, user_id=current_user.id)

@router.get("/get_user_channels")
async def get_user_channel(db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    return rep_channels.get_user_channels(db=db_conn, user_id=current_user.id)

@router.post("/join_channel")
async def join_channel(data_in: SCH_Join_Channel, db_conn: Session = Depends(deps.get_db), current_user: UserMe = Depends(deps.get_current_active_user)):
    return rep_channels.join_channel(db=db_conn, channel_name=data_in.quick_name, user_id=current_user.id)

