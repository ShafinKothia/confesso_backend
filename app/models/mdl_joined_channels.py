from sqlalchemy.sql.expression import true
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import Boolean

from app.db.base_class import Base

class MDL_Joined_Channels(Base):
    __tablename__ = "joined_channels"

    id = Column(UUID, primary_key=true)
    channel_id = Column(UUID)    
    user_id = Column(UUID)    