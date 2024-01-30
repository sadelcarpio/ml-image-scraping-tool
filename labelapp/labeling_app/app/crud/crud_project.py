import uuid

from sqlmodel import Session, select

from app.crud.base import CRUD
from app.models.projects import ProjectModel
from app.models.urls import UrlModel
from app.models.users import UserModel
from app.schemas.projects import ProjectCreate, ProjectUpdate


class CRUDProject(CRUD[ProjectModel, ProjectCreate, ProjectUpdate]):

    def get_urls(self, session: Session, project_id: int, skip: int = 0, limit: int = 5):
        """Get the urls for a given project id"""
        urls = session.exec(
            select(UrlModel).join(ProjectModel).where(ProjectModel.id == project_id).limit(limit).offset(skip))
        return urls

    def get_user_urls(self, session: Session, project_id: int, user_id: str, skip: int = 0, limit: int = 5):
        """Get urls for a user in a project."""
        urls = session.exec(
            select(UrlModel).join(ProjectModel)
            .join(UserModel)
            .where(ProjectModel.id == project_id,
                   UserModel.id == user_id).limit(limit).offset(skip))
        return urls

    def get_projects_by_owner(self, session: Session, owner_id: str):
        """Get the projects owned by a given user."""
        pass

    def create_with_users(self, session: Session, obj_in: ProjectCreate, user_ids: list[uuid.UUID]) -> ProjectModel:
        created_project = self.create(session, obj_in)
        project_users = session.exec(select(UserModel).where(UserModel.id.in_(user_ids))).all()
        created_project.users = project_users
        session.add(created_project)
        session.commit()
        session.refresh(created_project)
        return created_project
