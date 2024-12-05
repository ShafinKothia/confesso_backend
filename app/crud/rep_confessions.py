from unicodedata import category
from app.schemas.sch_confessions import SCH_Create_Confession, SCH_Get_Unapproved_Confessions, SCH_Get_Confession_Pages, SCH_Get_Confession_Pages_By_Channel_Id, SCH_Get_Confession_By_Id, SCH_Get_Confessions, SCH_Get_Confessions_By_Channel_Id
from socket import MsgFlag
from fastapi import datastructures, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import math

from sqlalchemy.dialects.postgresql.base import UUID
from app.models.mdl_confessions import MDL_Confessions
from typing import Any, Dict, Optional, Union
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
import uuid
from app.crud.rep_owner_channels import rep_owner_channels

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from sqlalchemy import create_engine

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


class CRUDConfessions(CRUDBase[MDL_Confessions, null, null]):
    def get_confessions(self, data_in: SCH_Get_Confessions, db: Session) -> Any:
        # print(type(data_in))
        # print(data_in)
        if data_in.limit is not None:
            if data_in.skip is not None:
                confessions_skipped = (data_in.skip - 1) * data_in.limit
                data = db.query(self.model).offset(confessions_skipped).limit(data_in.limit).all()
                return data
            else:
                data = db.query(self.model).limit(data_in.limit).all()
                return data
        else:
            data = db.query(self.model).all()
            return data
        
    def get_confessions_by_channel_id(self, data_in: SCH_Get_Confessions_By_Channel_Id, db: Session) -> Any:
        # print(type(data_in))
        # print(data_in)
        def get_confessions():
            if data_in.limit is not None:
                if data_in.skip is not None:
                    confessions_skipped = (data_in.skip - 1) * data_in.limit
                    data = db.query(self.model).filter(MDL_Confessions.channel_id == str(data_in.channel_id)).filter(MDL_Confessions.approved == True).offset(confessions_skipped).limit(data_in.limit).all()
                    return data
                else:
                    data = data = db.query(self.model).filter(MDL_Confessions.channel_id == str(data_in.channel_id)).filter(MDL_Confessions.approved == True).limit(data_in.limit).all()
                    return data
            else:
                data = data = db.query(self.model).filter(MDL_Confessions.channel_id == str(data_in.channel_id)).filter(MDL_Confessions.approved == True).all()
                return data
        total_data = get_confessions()
        return total_data

        

    def get_confession_by_id(self, db: Session, confession_id:     UUID ) -> Any:
        
        data = db.query(self.model).filter(MDL_Confessions.id == str(confession_id)).first()
        return data    

    def get_no_of_confession_pages(self, db: Session, data_in: SCH_Get_Confession_Pages ) -> Any:

        
        data = db.query(self.model).all()
        round_pages = len(data) / data_in.limit
        no_of_pages = math.ceil(round_pages)
        return no_of_pages

    def get_no_of_confession_pages_by_channel_id(self, db: Session, data_in: SCH_Get_Confession_Pages_By_Channel_Id) -> Any:

        
        data = data = db.query(self.model).filter(MDL_Confessions.channel_id == str(data_in.channel_id)).all()
        round_pages = len(data) / data_in.limit
        no_of_pages = math.ceil(round_pages)
        return no_of_pages

    def get_unapproved_confessions(self, db: Session, data_in: SCH_Get_Unapproved_Confessions, user_id: UUID) -> Any:
        is_owner = rep_owner_channels.is_owner(db=db, owner_id=user_id, channel_id=data_in.channel_id)
        if not is_owner:
            raise HTTPException(
                status_code=401,
                detail="Not owner of this channel"
            )
        if data_in.limit is not None:
            if data_in.skip is not None:
                confessions_skipped = (data_in.skip - 1) * data_in.limit
                data = db.query(self.model).filter(MDL_Confessions.channel_id == str(data_in.channel_id)).filter(MDL_Confessions.approved == False).offset(confessions_skipped).limit(data_in.limit).all()
                return data
            else:
                data = data = db.query(self.model).filter(MDL_Confessions.channel_id == str(data_in.channel_id)).filter(MDL_Confessions.approved == False).limit(data_in.limit).all()
                return data
        else:
            data = data = db.query(self.model).filter(MDL_Confessions.channel_id == str(data_in.channel_id)).filter(MDL_Confessions.approved == False).all()
            return data
        
    async def add_image(self, db: Session, *,
                      image_file: UploadFile = File(...), confession_id: UUID) -> Any:

        file = image_file
        id = uuid.uuid4()
        file.filename = f"{id}.png"
        contents = await file.read()

        engine.execute(f"""update confessions set image_path = '{id}' where id = '{str(confession_id)}'""")
        with open(f"D:/confessoimages/{file.filename}", "wb") as f:
            f.write(contents)

    def get_image(self, db: Session, *,
                       image_id: UUID) -> Any:

        return FileResponse(path=f"D:/confessoimages/{image_id}.png")

    def create_confession(self, db: Session, *,
                      confession_in: SCH_Create_Confession) -> Any:
        
        id = uuid.uuid4()
        db_obj = MDL_Confessions(id=str(id),
                                confession=confession_in.confession,
                                channel_id = str(confession_in.channel_id),
                                approved = False,
                                )
        db.add(db_obj)
        db.commit()
        return {"id": str(id)}
    
    def approve_confession(self, db: Session, *,
                      confession_id: UUID) -> Any:
        engine.execute(f"""update confessions set approved = 'true' where id = '{str(confession_id)}'""")
        return True


rep_confessions = CRUDConfessions(MDL_Confessions)
