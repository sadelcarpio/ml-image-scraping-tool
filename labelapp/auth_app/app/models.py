import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import Field

from app.schemas import UserBase


class UserModel(UserBase, table=True):
    __tablename__ = "users"
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str
    hashed_password: str
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
