import uuid

from pydantic import EmailStr, field_validator
from pydantic_core.core_schema import ValidationInfo
from sqlmodel import SQLModel, Field, AutoString


class UserBase(SQLModel):
    username: str = Field(unique=True, nullable=False)
    email: EmailStr = Field(unique=True, nullable=False, sa_type=AutoString)
    is_admin: bool = False


class UserRead(SQLModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    full_name: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str, values: ValidationInfo) -> str:
        username = values.data.get("username")
        if username in password:
            raise ValueError("Password can't contain username information.")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if len(password) > 20:
            raise ValueError("Password must be at most 20 characters.")
        return password


class UserUpdate(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
