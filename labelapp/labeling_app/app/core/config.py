from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

from pydantic import PostgresDsn, field_validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    INSTANCE_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    @classmethod
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+pg8000",
            username=values.data.get("DB_USER"),
            password=values.data.get("DB_PASSWORD"),
            host=values.data.get("INSTANCE_NAME"),
            path=f"{values.data.get('DB_NAME') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()
