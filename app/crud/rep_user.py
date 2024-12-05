from typing import Any, Dict, Optional, Union
from bcrypt import re
from graphene import UUID

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.mdl_user import MDL_User
from app.schemas.sch_user import UserCreate
import uuid
import re
from sqlalchemy import create_engine
from app.core.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

class CRUDUser(CRUDBase[MDL_User, null, null]):


    def get_users(self, db: Session) -> Any:
        return db.query(self.model).all()

    def get_user_by_id(self, db: Session, id: UUID) -> Any:
        user = db.query(self.model).filter(MDL_User.id == str(id)).first()
        return user

    def get_user_by_username(self, db: Session, username: str) -> Any:
        user = db.query(self.model).filter(MDL_User.username == username).first()
        return user

    def verify_user(self, db:Session, id: UUID) -> Any:
        engine.execute(f"""update anx_users set is_active = True where id = '{id}'""")
    def create_user(self, db: Session, create_data: UserCreate, hashed_password: str) -> Any:

        user_id_uuid = uuid.uuid4()
        user_id = str(user_id_uuid)
        print(user_id) 
        db_obj = MDL_User(
            id = user_id,
            username = create_data.username,
            hashed_password= hashed_password,
            is_active = True,
        )
        db.add(db_obj)
        db.commit()
        
        # # print(self.get_user_by_id(db=db, id=id))
        return self.get_user_by_id(db=db, id=user_id)
        

rep_user = CRUDUser(MDL_User)
