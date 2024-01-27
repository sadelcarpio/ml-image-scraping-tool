from sqlmodel import SQLModel, Field


class UrlBase(SQLModel):
    gcs_url: str = Field(unique=True, nullable=False)


class UrlResponse(UrlBase):
    id: int
