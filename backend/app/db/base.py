import uuid

from datetime import datetime
from typing import Dict, Any


from sqlalchemy import Column, UUID, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id = Column(
        UUID(as_uuid=False),
        primary_key=True,
        default=uuid.uuid4,  
        index=True,
        unique=True,
    )

    def get_look(self) -> Dict[str, Any]:
        """Return model attributes as dictionary"""
        return {
            col.name: self._serialize_value(getattr(self, col.name))
            for col in self.__table__.columns
        }

    def _serialize_value(self, value: Any) -> Any:
        """Serialize complex types for dictionary"""
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, uuid.UUID):
            return str(value)
        return value
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

