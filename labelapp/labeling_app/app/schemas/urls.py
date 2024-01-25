from datetime import datetime

from sqlmodel import SQLModel, Field


class UrlBase(SQLModel):
    gcs_url: str = Field(unique=True, nullable=False)


class UrlResponse(UrlBase):
    id: int


class UrlUpdated(UrlBase):
    id: int
    updated_at: datetime


class LabeledImage(SQLModel):
    format: str


class LabeledImageCls(SQLModel):
    value: int
