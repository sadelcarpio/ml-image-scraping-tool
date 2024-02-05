from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.api.deps import SessionDep
from app.crud.base import CRUD
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUD[UserModel, UserCreate, UserUpdate]):

    def get_by_email(self, email: str):
        pass

    def get_projects_by_owner(self, owner_id: str):
        """Get the projects owned by a given user."""
        pass


def get_users_crud(session: SessionDep):
    return CRUDUser(UserModel, session)


CRUDUserDep = Annotated[CRUDUser, Depends(get_users_crud)]
