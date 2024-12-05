from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class VWPageTableColumn(Base):
    __tablename__ = "fnin_v_page_table_columns"
    id = Column(UUID , primary_key=True)
    fnin_company_id = Column(UUID)
    fnin_page_id = Column(UUID)
    name = Column(String)
    fnin_table_id = Column(UUID)    
    display_name = Column(String)
    column_name = Column(String)
    table_name = Column(String)
    fnin_datatype_id = Column(UUID)
    fnin_control_id = Column(UUID)
