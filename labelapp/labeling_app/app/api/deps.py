from sqlmodel import Session

from typing import Generator
from app.db.engine import engine


def get_db() -> Generator:
    with Session(engine) as session:
        yield session
