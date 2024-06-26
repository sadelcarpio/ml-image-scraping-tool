import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field


class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str


class ProjectModel(SQLModel, table=True):
    __tablename__ = "projects"
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str
    last_processed: datetime = Field(default_factory=lambda: datetime.utcfromtimestamp(0))
    keywords: str
    owner_id: uuid.UUID = Field(default=None, foreign_key="users.id")
