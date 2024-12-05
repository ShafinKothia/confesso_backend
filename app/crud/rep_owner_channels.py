from app.schemas.sch_owner_channels import SCH_Get_Owner_Channel_By_Id, SCH_Get_Owner_Channels
from socket import MsgFlag
from fastapi import datastructures

from sqlalchemy.dialects.postgresql.base import UUID
from app.models.mdl_owner_channels import MDL_Owner_Channels
from typing import Any, Dict, Optional, Union
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
import uuid

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from sqlalchemy import create_engine

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


class CRUDFunction(CRUDBase[MDL_Owner_Channels, null, null]):
    def get_owner_channels(self, data_in: SCH_Get_Owner_Channels, db: Session) -> Any:
        print(type(data_in.skip))
        if data_in.skip is not None:
            posts_skipped = (data_in.skip - 1) * 20
            data = db.query(self.model).offset(posts_skipped).limit(20).all()
            return data
        else:
            data = db.query(self.model).all()
            return data

    def get_owner_channel_by_id(self, db: Session, data_in:     SCH_Get_Owner_Channel_By_Id ) -> Any:
        
        data = db.query(self.model).filter(MDL_Owner_Channels.id == str(data_in.id)).first()
        return data
    
    def get_owner_channels_by_owner_id(self, db: Session, owner_in:     UUID ) -> Any:
        
        data = db.query(self.model).filter(MDL_Owner_Channels.owner_id == str(owner_in)).all()
        return data

    def is_owner(self, db: Session, *,
                    owner_id: UUID, channel_id: UUID) -> Any:
        exists = db.query(self.model).filter(MDL_Owner_Channels.owner_id == str(owner_id)).filter(MDL_Owner_Channels.channel_id == str(channel_id)).first() is not None
        print(exists)
        return exists

    def create_owner_channel(self, db: Session, *,
                    owner_id: UUID, channel_id: UUID) -> Any:
        db_obj = MDL_Owner_Channels(id=str(uuid.uuid4()),
                                owner_id = str(owner_id),
                                channel_id = str(channel_id)
                    )
        db.add(db_obj)
        db.commit()
        return True


rep_owner_channels = CRUDFunction(MDL_Owner_Channels)
