from pydantic import EmailStr
from sqlmodel import SQLModel, Field, AutoString


class UserBase(SQLModel):
    username: str = Field(unique=True, nullable=False)
    full_name: str
    email: EmailStr = Field(unique=True, nullable=False, sa_type=AutoString)
