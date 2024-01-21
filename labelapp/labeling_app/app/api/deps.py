from fastapi import Depends
from sqlalchemy.sql.functions import current_user
from sqlmodel import Session, select

from typing import Generator, Annotated
from app.db.engine import engine
from app.models import UserModel


def get_db() -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_current_user(session: SessionDep) -> UserModel:
    user = session.exec(select(UserModel)).first()
    return user


CurrentUser = Annotated[UserModel, Depends(get_current_user)]
