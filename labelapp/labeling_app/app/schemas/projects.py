import uuid

from sqlmodel import SQLModel, Field

from app.models.extras import LabelModel
from app.models.users import UserModel
from app.schemas.extras import LabelRead


class ProjectBase(SQLModel):
    name: str = Field(unique=True, nullable=False)
    keywords: str = Field(nullable=False)
    description: str
    task_type: str


class ProjectRead(ProjectBase):
    owner_id: uuid.UUID
    labels: list["LabelRead"] = []


class ProjectCreate(ProjectRead):
    users: list["UserModel"]
    labels: list["LabelModel"] = []


class ProjectUpdate(ProjectBase):
    name: str | None = None
    keywords: str | None = None
    description: str | None = None
    users: list["UserModel"] | None = None
