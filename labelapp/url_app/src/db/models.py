import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UUID

from src.db.base import Base


class UrlModel(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    gcs_url = Column(String, unique=True, nullable=False)
    hashed_url = Column(String(64), nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
