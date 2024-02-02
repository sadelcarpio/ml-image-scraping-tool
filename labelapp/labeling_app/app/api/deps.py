from typing import Generator, Annotated

from fastapi import Depends
from fastapi import HTTPException
from sqlmodel import Session, select

from app.db.engine import EngineDep
from app.models.users import UserModel


def get_db(engine: EngineDep) -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


# TODO: change with actual user authentication
def get_current_user(session: SessionDep) -> UserModel:
    user = session.exec(select(UserModel).where(UserModel.is_admin == False)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Current user not found.")
    return user


CurrentUser = Annotated[UserModel, Depends(get_current_user)]
