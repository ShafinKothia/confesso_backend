from sqlalchemy.sql.expression import true
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import Boolean

from app.db.base_class import Base

class MDL_Confessions(Base):
    __tablename__ = "confessions"

    id = Column(UUID, primary_key=true)
    confession = Column(String)
    channel_id = Column(UUID)
    approved= Column(Boolean)
    image_path = Column(String)
    
    