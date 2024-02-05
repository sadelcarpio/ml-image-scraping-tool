from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, select

from app.api.deps import SessionDep
from app.crud.base import CRUD
from app.models.extras import UserProjectModel
from app.models.projects import ProjectModel
from app.models.urls import UrlModel
from app.models.users import UserModel
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectCreateWithUsers


class CRUDProject(CRUD[ProjectModel, ProjectCreate, ProjectUpdate]):

    def get_urls(self, project_id: int, skip: int = 0, limit: int = 5):
        """Get the urls for a given project id"""
        urls = self.session.exec(
            select(UrlModel).join(ProjectModel).where(ProjectModel.id == project_id).limit(limit).offset(skip))
        return urls

    def get_user_urls(self, project_id: int, user_id: str, skip: int = 0, limit: int = 5):
        """Get urls for a user in a project."""
        urls = self.session.exec(
            select(UrlModel)
            .where(UrlModel.project_id == project_id,
                   UrlModel.user_id == user_id).limit(limit).offset(skip))
        return urls

    def get_users_by_project(self, project_id: int, skip: int = 0, limit: int = 5):
        """Get all users that belong to a project."""
        users = self.session.exec(select(UserModel)
                                  .join(UserProjectModel)
                                  .join(ProjectModel)
                                  .where(ProjectModel.id == project_id)
                                  .limit(limit)
                                  .offset(skip))
        return users

    def create_with_users(self, obj_in: ProjectCreateWithUsers) -> ProjectModel:
        project_create = ProjectCreate.model_validate(obj_in)
        user_ids = obj_in.user_ids
        created_project = self.create(project_create)
        project_users = self.session.exec(select(UserModel).where(UserModel.id.in_(user_ids))).all()
        created_project.users = project_users
        self.session.add(created_project)
        self.session.commit()
        self.session.refresh(created_project)
        return created_project

    def add_user(self, project: ProjectModel, user: UserModel):
        project.users.append(user)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)

    def remove_user(self, project: ProjectModel, user: UserModel):
        project.users.remove(user)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)


def get_projects_crud(session: SessionDep):
    return CRUDProject(ProjectModel, session)


CRUDProjectDep = Annotated[CRUDProject, Depends(get_projects_crud)]
