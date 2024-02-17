from typing import Annotated

from fastapi import Depends
from sqlmodel import select

from app.api.deps import SessionDep
from app.crud.base import CRUD
from app.models.extras import UserProjectModel
from app.models.projects import ProjectModel
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserUpdate
from app.security.passwords import get_password_hash


class CRUDUser(CRUD[UserModel, UserCreate, UserUpdate]):

    def get_by_username(self, username: str) -> UserModel:
        user = self.session.exec(select(UserModel).where(UserModel.username == username)).first()
        return user

    def create_with_pwd_hashing(self, obj_in: UserCreate) -> UserModel:
        obj_in_data = {key: value for key, value in obj_in if key != "password"}
        hashed_password = get_password_hash(obj_in.password)
        db_user = UserModel(**obj_in_data, hashed_password=hashed_password)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_projects_by_owner(self, owner_id: str, skip: int = 0, limit: int = 5):
        """Get the projects owned by a given user."""
        projects = self.session.exec(select(ProjectModel)
                                     .join(UserModel)
                                     .where(ProjectModel.owner_id == owner_id)
                                     .limit(limit)
                                     .offset(skip))
        return projects

    def get_assigned_projects(self, user_id: str, skip: int = 0, limit: int = 5):
        projects = self.session.exec(select(ProjectModel)
                                     .join(UserProjectModel)
                                     .join(UserModel)
                                     .where(UserModel.id == user_id)
                                     .limit(limit)
                                     .offset(skip))
        return projects


def get_users_crud(session: SessionDep):
    return CRUDUser(UserModel, session)


CRUDUserDep = Annotated[CRUDUser, Depends(get_users_crud)]
