from pydantic import EmailStr
from sqlmodel import SQLModel, Field, AutoString


class UserBase(SQLModel):
    username: str = Field(unique=True, nullable=False)
    email: EmailStr = Field(unique=True, nullable=False, sa_type=AutoString)
    is_admin: bool = False


class UserRead(SQLModel):
    username: str
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    full_name: str
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
