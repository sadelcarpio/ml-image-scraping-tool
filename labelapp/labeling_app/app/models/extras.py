import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import SQLModel, Field, Relationship

from app.models.urls import UrlModel
from app.schemas.extras import LabelRead

if TYPE_CHECKING:
    from app.models.projects import ProjectModel
    from app.models.urls import UrlModel


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


class LabeledUrlModel(SQLModel, table=True):
    __tablename__ = "labeled_urls"
    id: int | None = Field(default=None, primary_key=True, index=True)
    url_id: int | None = Field(sa_column=Column('url_id', ForeignKey("urls.id", ondelete="CASCADE")))
    url: Optional["UrlModel"] = Relationship(back_populates="labeled_url")
    label: str | None = Field(default=None)  # label name
    value_int: int | None = Field(default=None)  # 0-1 for multilabel classification, also for regression
    value_float: float | None = Field(default=None)  # For regression
