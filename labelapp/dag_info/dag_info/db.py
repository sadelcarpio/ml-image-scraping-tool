import os

from sqlmodel import create_engine, Session

engine = create_engine(f"postgresql+pg8000://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}"
                       f"@{os.environ.get('INSTANCE_NAME')}/{os.environ.get('DB_NAME')}")


def get_session():
    with Session(engine) as session:
        yield session
