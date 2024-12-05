from unicodedata import category
from app.schemas.sch_channels import SCH_Create_Channel, SCH_Get_Channel_By_Id, SCH_Get_Channels
from socket import MsgFlag
from fastapi import datastructures, HTTPException
import math
import random
from sqlalchemy.dialects.postgresql.base import UUID
from app.models.mdl_channels import MDL_Channels
from typing import Any, Dict, Optional, Union
from app.core.config import settings
from sqlalchemy.orm import Session

from sqlalchemy.sql.expression import null
import uuid
from app.crud.rep_joined_channels import rep_joined_channels
from app.crud.rep_owner_channels import rep_owner_channels

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from sqlalchemy import create_engine

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


class CRUDChannels(CRUDBase[MDL_Channels, null, null]):
    def get_channels(self, data_in: SCH_Get_Channels, db: Session) -> Any:
        # print(type(data_in))
        # print(data_in)
        if data_in.limit is not None:
            if data_in.skip is not None:
                posts_skipped = (data_in.skip - 1) * data_in.limit
                data = db.query(self.model).offset(posts_skipped).limit(data_in.limit).all()
                return data
            else:
                data = db.query(self.model).limit(data_in.limit).all()
                return data
        else:
            data = db.query(self.model).all()
            return data

    def get_channel_by_id(self, db: Session, channel_id:     UUID ) -> Any:
        
        data = db.query(self.model).filter(MDL_Channels.id == str(channel_id)).first()
        return data
    
    def is_channel(self, db: Session, channel_id:     UUID ) -> Any:
        
        data = db.query(self.model).filter(MDL_Channels.id == str(channel_id)).first()
        if data is None:
            return False
        else:
            return True

    def create_channel(self, db: Session, *,
                      channel_in: SCH_Create_Channel, user_id: UUID) -> Any:
        quick_name = channel_in.name.replace(" ", '').lower() + '_' + str(random.randint(0000, 1000)).rjust(4, "0")
        channel_id = uuid.uuid4()
        db_obj = MDL_Channels(id=str(channel_id),
                                name=channel_in.name,
                                quick_name=quick_name,
                                images_allowed=channel_in.images_allowed
                                )
        db.add(db_obj)
        db.commit()
        rep_owner_channels.create_owner_channel(db=db, owner_id=user_id, channel_id=channel_id)
        return {"quick_name": quick_name}
    
    def get_self_channels(self, db: Session, *,
                      user_id: UUID) -> Any:
        data = rep_owner_channels.get_owner_channels_by_owner_id(db=db, owner_in=user_id)
        id_list = [result.channel_id for result in data]
        total_data=db.query(self.model).filter(MDL_Channels.id.in_(id_list)).all()

        return total_data
    
    def get_user_channels(self, db: Session, *,
                      user_id: UUID) -> Any:
        joined_channels_ids = rep_joined_channels.get_joined_channels_by_user_id(db=db, id=user_id)
        joined_channels = []
        for i in joined_channels_ids:
            joined_channels.append(self.get_channel_by_id(db=db, channel_id=i.channel_id)
        )
        return joined_channels
    
        
    
    def join_channel(self, db: Session, *, channel_name: str, user_id: UUID) -> Any:
        channel_exists = db.query(self.model).filter(MDL_Channels.quick_name == str(channel_name)).first()
        if not channel_exists:
            raise HTTPException(
                status_code=404,
                detail="Channel Doesnt Exist"
            )

        is_joined_channel = rep_joined_channels.is_joined_channel(db=db, user_id=user_id, channel_id=channel_exists.id)
        if is_joined_channel:
            raise HTTPException(
                status_code=409,
                detail="Already Joined Channel"
            )
        
        rep_joined_channels.create_joined_channel(db=db, channel_id=channel_exists.id, user_id=user_id)


rep_channels = CRUDChannels(MDL_Channels)
