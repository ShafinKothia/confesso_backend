from unicodedata import category
from isort import code
from sqlalchemy.sql.expression import true
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import Boolean

from app.db.base_class import Base

class MDL_Owner_Channels(Base):
    __tablename__ = "owner_channels"

    id = Column(UUID, primary_key=true)
    owner_id = Column(UUID)
    channel_id = Column(UUID)
    #add other columns here
    
    
