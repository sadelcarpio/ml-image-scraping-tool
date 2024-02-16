from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import create_engine, Session

from app.config import SettingsDep


def get_engine(settings: SettingsDep) -> Engine:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    return engine


EngineDep = Annotated[Engine, Depends(get_engine)]


def get_db(engine: EngineDep) -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
