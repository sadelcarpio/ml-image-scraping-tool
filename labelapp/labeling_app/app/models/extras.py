import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import SQLModel, Field, Relationship

from app.schemas.extras import LabelRead

if TYPE_CHECKING:
    from app.models.projects import ProjectModel


class UserProjectModel(SQLModel, table=True):
    __tablename__ = "users_projects"
    user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, foreign_key="users.id", primary_key=True)
    project_id: int | None = Field(default=None, foreign_key="projects.id", primary_key=True)
    assigned_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    current_url: int | None = Field(default=None, foreign_key="urls.id")


class LabelModel(LabelRead, table=True):
    __tablename__ = "labels"
    id: int | None = Field(default=None, primary_key=True)
    project_id: int | None = Field(sa_column=Column('project_id',
                                                    Integer,
                                                    ForeignKey("projects.id", ondelete="CASCADE")))
    project: Optional["ProjectModel"] = Relationship(back_populates="labels")
