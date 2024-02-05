from sqlmodel import Session

from app.crud.base import CRUD
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUD[UserModel, UserCreate, UserUpdate]):

    def get_by_email(self, session: Session, email: str):
        pass

    def get_projects_by_owner(self, session: Session, owner_id: str):
        """Get the projects owned by a given user."""
        pass
