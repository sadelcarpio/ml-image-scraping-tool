import os

from sqlmodel import create_engine, Session

engine = create_engine(f"postgresql+pg8000://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
                       f"@localhost:5432/{os.environ['DB_NAME']}")


def get_session():
    with Session(engine) as session:
        yield session
