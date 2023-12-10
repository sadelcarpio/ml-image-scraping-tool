from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from src.db.base import Base


class UrlModel(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    gcs_url = Column(String, unique=True)
    hashed_url = Column(String(64))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    updated_at = Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
