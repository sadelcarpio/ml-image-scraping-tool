from sqlmodel import Session

from app.crud.base import CRUD
from app.models import ProjectModel
from app.schemas.projects import ProjectCreate, ProjectUpdate


class CRUDProject(CRUD[ProjectModel, ProjectCreate, ProjectUpdate]):
    def get_urls(self, session: Session, project_id: int):
        pass

    def get_user_urls(self, session: Session, project_id: int, user_id: str):
        pass

    def get_projects_by_owner(self, session: Session, owner_id: str):
        pass
