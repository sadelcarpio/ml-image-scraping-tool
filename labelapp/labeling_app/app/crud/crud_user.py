from typing import Annotated

from fastapi import Depends
from sqlmodel import select

from app.api.deps import SessionDep
from app.crud.base import CRUD
from app.models.extras import UserProjectModel
from app.models.projects import ProjectModel
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUD[UserModel, UserCreate, UserUpdate]):

    def get_by_email(self, email: str):
        pass

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
