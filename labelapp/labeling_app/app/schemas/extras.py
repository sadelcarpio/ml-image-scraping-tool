from sqlmodel import SQLModel


class LabelRead(SQLModel):
    name: str
