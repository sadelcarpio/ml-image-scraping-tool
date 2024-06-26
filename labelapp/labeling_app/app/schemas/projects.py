import re
import uuid

from pydantic import field_validator
from sqlmodel import SQLModel, Field

from app.models.extras import LabelModel
from app.schemas.extras import LabelRead
from app.schemas.users import UserRead


class ProjectBase(SQLModel):
    name: str = Field(unique=True, nullable=False)
    keywords: str = Field(nullable=False)
    description: str
    task_type: str

    @field_validator("name")
    @classmethod
    def validate_project_name(cls, project_name: str) -> str:
        pattern = r"^\w+[\w-]+$"
        if bool(re.match(pattern, project_name)):
            return project_name
        else:
            raise ValueError("Invalid project name. Project name must have the format ^\w+[\w-]+$ "
                             "(only letters, numbers, dash and underscores")


class ProjectRead(ProjectBase):
    owner_id: uuid.UUID
    labels: list["LabelRead"] = []


class ProjectReadWithUsers(ProjectRead):
    users: list["UserRead"]


class ProjectCreate(ProjectRead):
    labels: list["LabelModel"] = []


class ProjectCreateWithUsers(ProjectBase):
    labels: list["LabelRead"] = []
    user_ids: list[uuid.UUID]

    @field_validator("user_ids")
    @classmethod
    def validate_user_ids_notempty(cls, user_ids: list) -> list:
        if not len(user_ids):
            raise ValueError("Can't create a project without users.")
        return user_ids


class ProjectUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
