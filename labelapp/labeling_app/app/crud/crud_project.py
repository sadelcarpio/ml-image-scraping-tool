from uuid import UUID

from sqlmodel import Session, select

from app.crud.base import CRUD
from app.models.projects import ProjectModel
from app.models.urls import UrlModel
from app.models.users import UserModel
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectCreateWithUsers


class CRUDProject(CRUD[ProjectModel, ProjectCreate, ProjectUpdate]):

    def get_urls(self, session: Session, project_id: int, skip: int = 0, limit: int = 5):
        """Get the urls for a given project id"""
        urls = session.exec(
            select(UrlModel).join(ProjectModel).where(ProjectModel.id == project_id).limit(limit).offset(skip))
        return urls

    def get_user_urls(self, session: Session, project_id: int, user_id: str, skip: int = 0, limit: int = 5):
        """Get urls for a user in a project."""
        urls = session.exec(
            select(UrlModel)
            .where(UrlModel.project_id == project_id,
                   UrlModel.user_id == user_id).limit(limit).offset(skip))
        return urls

    def get_projects_by_owner(self, session: Session, owner_id: str):
        """Get the projects owned by a given user."""
        pass

    def create_with_users(self, session: Session, obj_in: ProjectCreateWithUsers) -> ProjectModel:
        project_create = ProjectCreate.from_orm(obj_in)
        user_ids = obj_in.user_ids
        created_project = self.create(session, project_create)
        project_users = session.exec(select(UserModel).where(UserModel.id.in_(user_ids))).all()
        created_project.users = project_users
        session.add(created_project)
        session.commit()
        session.refresh(created_project)
        return created_project
