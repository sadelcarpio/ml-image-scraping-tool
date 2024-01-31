from sqlmodel import Session, select

from app.crud.base import CRUD
from app.models.extras import UserProjectModel
from app.models.projects import ProjectModel
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUD[UserModel, UserCreate, UserUpdate]):

    def get_by_email(self, session: Session, email: str):
        pass

    def get_users_by_project(self, session: Session, project_id: int):
        """Get all users that belong to a project."""
        users = session.exec(select(UserModel)
                             .join(UserProjectModel)
                             .join(ProjectModel)
                             .where(ProjectModel.id == project_id))
        return users
