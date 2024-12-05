
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class Company(Base):
    __tablename__ = "fnin_companies"

    id = Column(UUID , primary_key=True)
    name = Column(String)
    prefix = Column(String)