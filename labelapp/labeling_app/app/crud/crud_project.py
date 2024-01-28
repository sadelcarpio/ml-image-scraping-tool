from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app.crud.base import CRUD
from app.models import ProjectModel, LabelModel
from app.schemas.projects import ProjectCreate, ProjectUpdate


class CRUDProject(CRUD[ProjectModel, ProjectCreate, ProjectUpdate]):

    def create_with_labels(self, session: Session, obj_in: ProjectCreate, labels: list[LabelModel]):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.Model(**obj_in_data, labels=labels)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_urls(self, session: Session, project_id: int):
        pass

    def get_user_urls(self, session: Session, project_id: int, user_id: str):
        pass

    def get_projects_by_owner(self, session: Session, owner_id: str):
        pass
