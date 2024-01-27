from sqlmodel import SQLModel, Field


class ProjectBase(SQLModel):
    name: str = Field(unique=True, nullable=False)
    keywords: str = Field(nullable=False)
    description: str


class ProjectCreate(ProjectBase):
    owner_id: str | None


class ProjectUpdate(ProjectBase):
    name: str | None = None
    keywords: str | None = None
    description: str | None = None
