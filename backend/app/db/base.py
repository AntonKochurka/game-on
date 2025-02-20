from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())