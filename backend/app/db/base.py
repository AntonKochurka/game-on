import uuid

from sqlalchemy import Column, UUID, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  
        index=True,
        unique=True,
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

from .models.user import User