import uuid

from sqlmodel import SQLModel, Field


class UrlBase(SQLModel):
    gcs_url: str = Field(unique=True, nullable=False)
    labeled: bool = Field(default=False)


class UrlRead(UrlBase):
    id: int
    user_id: uuid.UUID
