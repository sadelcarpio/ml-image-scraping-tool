from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import create_engine

from app.core.config import SettingsDep


def get_engine(settings: SettingsDep) -> Engine:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    return engine


EngineDep = Annotated[Engine, Depends(get_engine)]
