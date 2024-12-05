from sqlalchemy.sql.expression import true
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import Boolean

from app.db.base_class import Base

class MDL_Channels(Base):
    __tablename__ = "channels"

    id = Column(UUID, primary_key=true)
    name = Column(String)
    quick_name = Column(String)
    images_allowed = Column(Boolean)
