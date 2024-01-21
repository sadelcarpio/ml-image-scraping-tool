import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field, Relationship


class UrlModel(SQLModel, table=True):
    __tablename__ = "urls"
    id: int | None = Field(default=None, primary_key=True)
    gcs_url: str = Field(unique=True, nullable=False)
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    labeled: bool
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id")
    project_id: int | None = Field(default=None, foreign_key="projects.id")


class UserProjectModel(SQLModel, table=True):
    __tablename__ = "users_projects"
    id: int | None = Field(default=None, primary_key=True)
    user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, foreign_key="users.id", primary_key=True)
    project_id: int | None = Field(default=None, foreign_key="projects.id", primary_key=True)
    assigned_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)


class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    full_name: str
    email: str = Field(unique=True, nullable=False)
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    projects: list["ProjectModel"] = Relationship(back_populates="users", link_model=UserProjectModel)


class ProjectModel(SQLModel, table=True):
    __tablename__ = "projects"
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str
    keywords: str
    description: str
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    owner_id: uuid.UUID = Field(default=None, foreign_key="users.id")
    users: list[UserModel] = Relationship(back_populates="projects", link_model=UserProjectModel)
