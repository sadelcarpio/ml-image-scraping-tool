import uuid

from sqlmodel import SQLModel, Field

from app.models.extras import LabelModel


class ProjectBase(SQLModel):
    name: str = Field(unique=True, nullable=False)
    keywords: str = Field(nullable=False)
    description: str
    task_type: str


class ProjectRead(ProjectBase):
    owner_id: uuid.UUID
    labels: list["LabelModel"] = []


class ProjectCreate(ProjectBase):
    owner_id: uuid.UUID | None


class ProjectUpdate(ProjectBase):
    name: str | None = None
    keywords: str | None = None
    description: str | None = None
