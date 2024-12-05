from app.schemas.sch_ReplaceFileName import SCH_Create_ReplaceTitle, SCH_Get_ReplaceTitle_By_Id, SCH_Get_ReplaceTitles
from socket import MsgFlag
from fastapi import datastructures

from sqlalchemy.dialects.postgresql.base import UUID
from app.models.mdl_ReplaceFileName import MDL_ReplaceTitles
from typing import Any, Dict, Optional, Union
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
import uuid

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from sqlalchemy import create_engine

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


class CRUDFunction(CRUDBase[MDL_ReplaceTitles, null, null]):
    def get_ReplaceLowercases(self, data_in: SCH_Get_ReplaceTitles, db: Session) -> Any:
        print(type(data_in.skip))
        if data_in.skip is not None:
            posts_skipped = (data_in.skip - 1) * 20
            data = db.query(self.model).offset(posts_skipped).limit(20).all()
            return data
        else:
            data = db.query(self.model).all()
            return data

    def get_ReplaceLowercase_by_id(self, db: Session, data_in:     SCH_Get_ReplaceTitle_By_Id ) -> Any:
        
        data = db.query(self.model).filter(MDL_ReplaceTitles.id == str(data_in.id)).first()
        return data

    def create_ReplaceLowercase(self, db: Session, *,
                      data_in: SCH_Create_ReplaceTitle) -> Any:
        db_obj = MDL_ReplaceTitles(id=str(uuid.uuid4()),
                                
                                
                                 )
        db.add(db_obj)
        db.commit()
        return "Done"


rep_ReplaceLowercases = CRUDFunction(MDL_ReplaceTitles)
