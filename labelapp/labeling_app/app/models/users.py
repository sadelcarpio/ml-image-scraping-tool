import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship

from app.models.extras import UserProjectModel
from app.schemas.users import UserBase

if TYPE_CHECKING:
    from app.models.projects import ProjectModel


class UserModel(UserBase, table=True):
    __tablename__ = "users"
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str
    full_name: str
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    projects: list["ProjectModel"] = Relationship(back_populates="users", link_model=UserProjectModel)
