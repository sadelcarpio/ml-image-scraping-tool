from typing import Generator, Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db.engine import EngineDep


def get_db(engine: EngineDep) -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
