from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class VWTableColumnDataTypeControl(Base):
    __tablename__ = "fnin_v_table_column_datatype_controls"
    id = Column(UUID , primary_key=True)
    name = Column(String)
    fnin_table_id = Column(UUID)    
    display_name = Column(String)
    column_name = Column(String)
    fnin_datatype_id = Column(UUID)
    fnin_control_id = Column(UUID)
