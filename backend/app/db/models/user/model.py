from app.db.base import Base, TimestampMixin
from sqlalchemy import Column, String

class User(Base, TimestampMixin):
    __tablename__ = 'users'

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")