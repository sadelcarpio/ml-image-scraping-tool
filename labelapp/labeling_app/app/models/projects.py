import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlmodel import Field, Relationship, Enum

from app.models.extras import UserProjectModel
from app.models.users import UserModel
from app.schemas.extras import TaskType
from app.schemas.projects import ProjectBase

if TYPE_CHECKING:
    from app.models.extras import LabelModel


class ProjectModel(ProjectBase, table=True):
    __tablename__ = "projects"
    id: int | None = Field(default=None, primary_key=True, index=True)
    task_type: str = Field(sa_column=Column(Enum(TaskType)))
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    last_processed: datetime = Field(default_factory=lambda: datetime.utcfromtimestamp(0))
    owner_id: uuid.UUID = Field(sa_column=Column('owner_id', ForeignKey("users.id", ondelete="CASCADE")))
    users: list[UserModel] = Relationship(back_populates="projects", link_model=UserProjectModel)
    labels: list["LabelModel"] = Relationship(back_populates="project",
                                              sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    owner: Optional[UserModel] = Relationship(back_populates="projects_owned")
