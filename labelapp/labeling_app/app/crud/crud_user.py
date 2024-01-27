from sqlmodel import Session

from app.crud.base import CRUD
from app.models import UserModel
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUD[UserModel, UserCreate, UserUpdate]):

    def get_by_email(self, session: Session, email: str):
        pass

    def get_users_by_project(self, session: Session, project_id: int, user_id: str):
        pass
