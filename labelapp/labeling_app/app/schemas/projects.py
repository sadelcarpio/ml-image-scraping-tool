import uuid

from pydantic import field_validator
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
    labels: list["LabelModel"] = []


class ProjectCreateWithUsers(ProjectCreate):
    user_ids: list[uuid.UUID]

    @field_validator("user_ids")
    @classmethod
    def validate_user_ids_notempty(cls, user_ids: list) -> list:
        if not len(user_ids):
            raise ValueError("Can't create a project without users.")
        return user_ids


class ProjectUpdate(ProjectBase):
    name: str | None = None
    keywords: str | None = None
    description: str | None = None
    users: list["UserModel"] | None = None
