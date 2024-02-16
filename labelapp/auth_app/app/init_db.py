from sqlmodel import SQLModel
from sqlmodel import Session

from app.config import Settings
from app.db import get_engine
from app.models import UserModel


def init_db():
    engine = get_engine(settings=Settings())
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        user = UserModel(username="sadelcarpio",
                         email="sadel@gmail.com",
                         full_name="Sergio DC",
                         is_admin=True,
                         hashed_password="iamnothashed")
        session.add(user)
        session.commit()
