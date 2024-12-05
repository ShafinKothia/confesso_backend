
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column


@as_declarative()
class Base:
    id = Column(UUID , primary_key=True)
    # created_by = Column(UUID)
    # created_dttm = Column(DateTime)
    # updated_by = Column(UUID)
    # updated_dttm = Column(DateTime)
    # is_active = Column(Boolean)

    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
