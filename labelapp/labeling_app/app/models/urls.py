import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
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
    labeled: bool = Field(default=False)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id")
    project_id: int | None = Field(default=None, foreign_key="projects.id")
