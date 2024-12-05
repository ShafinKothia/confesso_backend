from unicodedata import category
from socket import MsgFlag
from fastapi import datastructures
import math

from sqlalchemy.dialects.postgresql.base import UUID
from app.models.mdl_joined_channels import MDL_Joined_Channels
from typing import Any, Dict, Optional, Union
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
import uuid

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from sqlalchemy import create_engine

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


class CRUDJoinedChannels(CRUDBase[MDL_Joined_Channels, null, null]):

    def get_joined_channel_by_id(self, db: Session, id:     UUID ) -> Any:
        
        data = db.query(self.model).filter(MDL_Joined_Channels.id == str(id)).first()
        return data

    def create_joined_channel(self, db: Session, *,
                      channel_id: UUID, user_id: UUID ) -> Any:
        db_obj = MDL_Joined_Channels(id=str(uuid.uuid4()),
                                channel_id=str(channel_id),
                                user_id = str(user_id)
                                )
        db.add(db_obj)
        db.commit()
        return "Done"
    
    def get_joined_channels_by_user_id(self, db: Session, *, id: UUID) -> Any:
        data = db.query(self.model).filter(MDL_Joined_Channels.user_id == str(id)).all()
        return data

    def is_joined_channel(self, db: Session, *, channel_id: UUID, user_id: UUID) -> Any:
        data = db.query(self.model).filter(MDL_Joined_Channels.user_id == str(user_id)).filter(MDL_Joined_Channels.channel_id == str(channel_id)).first()
        if data is None:
            return False
        else:
            return True


rep_joined_channels = CRUDJoinedChannels(MDL_Joined_Channels)
