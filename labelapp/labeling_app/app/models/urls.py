import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey
from sqlmodel import Field

from app.schemas.urls import UrlBase


class UrlModel(UrlBase, table=True):
    __tablename__ = "urls"
    id: int | None = Field(default=None, primary_key=True)
    hashed_url: str = Field(unique=True, nullable=False)
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    user_id: uuid.UUID | None = Field(sa_column=Column('user_id', ForeignKey("users.id", ondelete="SET NULL")))
    project_id: int | None = Field(sa_column=Column('project_id', ForeignKey("projects.id", ondelete="CASCADE")))
