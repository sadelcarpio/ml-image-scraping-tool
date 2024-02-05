from fastapi import APIRouter, status

from app.api.deps import SessionDep
from app.crud import CRUDProject, CRUDUser
from app.models.projects import ProjectModel
from app.models.urls import UrlModel
from app.models.users import UserModel
from app.schemas.projects import ProjectRead, ProjectCreateWithUsers, ProjectUpdate
from app.schemas.urls import UrlRead
from app.schemas.users import UserRead

router = APIRouter(tags=["Projects Endpoints"])
project_crud = CRUDProject(ProjectModel)
users_crud = CRUDUser(UserModel)


@router.get("/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectRead)
def project_information(project_id: int, session: SessionDep) -> ProjectModel:
    """Fetch information from a certain project."""
    return project_crud.get(session, project_id)


@router.get("/{project_id}/{user_id}/urls", status_code=status.HTTP_200_OK, response_model=list[UrlRead])
def read_user_urls(project_id: int, user_id: str, session: SessionDep, skip: int = 0, limit: int = 5) -> list[UrlModel]:
    """Fetch urls assigned to a certain user in the project."""
    urls = project_crud.get_user_urls(session, project_id, user_id, skip=skip, limit=limit).all()
    return urls


@router.get("/{project_id}/urls", status_code=status.HTTP_200_OK, response_model=list[UrlRead])
def read_project_urls(project_id: int, session: SessionDep, skip: int = 0, limit: int = 5) -> list[UrlModel]:
    """Fetch all urls assigned to a given project."""
    urls = project_crud.get_urls(session, project_id, skip=skip, limit=limit).all()
    return urls


@router.get("/{project_id}/users", status_code=status.HTTP_200_OK, response_model=list[UserRead])
def read_users(project_id: int, session: SessionDep) -> list[UserModel]:
    """Fetch all users assigned to a given project."""
    return users_crud.get_users_by_project(session, project_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProjectRead)
def create_project(project: ProjectCreateWithUsers, session: SessionDep) -> ProjectModel:
    """Create a new project."""
    created_project = project_crud.create_with_users(session, project)
    return created_project


@router.put("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_project(project_id: int, project_updates: ProjectUpdate, session: SessionDep):
    """Edit some properties of a project"""
    project_to_update = project_crud.get(session, project_id)
    project_crud.update(session, project_to_update, project_updates)


@router.put("/{project_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_user(project_id: int, user_id: str, session: SessionDep):
    """Add a user to the project"""
    project_crud.add_user(session, users_crud, project_id, user_id)


@router.delete("/{project_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(project_id: int, user_id: str, session: SessionDep):
    """Remove a user from the project"""
    project_crud.remove_user(session, users_crud, project_id, user_id)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: SessionDep):
    """Delete a project."""
    project_crud.remove(session, project_id)
