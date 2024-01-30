from fastapi import APIRouter, status

from app.api.deps import SessionDep
from app.crud import CRUDProject, CRUDUser
from app.models.projects import ProjectModel
from app.models.users import UserModel
from app.schemas.projects import ProjectRead, ProjectCreate, ProjectCreateWithUsers
from app.schemas.urls import UrlRead
from app.schemas.users import UserRead

router = APIRouter(tags=["Projects Endpoints"])
project_crud = CRUDProject(ProjectModel)
users_crud = CRUDUser(UserModel)


@router.get("/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectRead)
def project_information(project_id: int, session: SessionDep):
    """Fetch information from a certain project."""
    return project_crud.get(session, project_id)


@router.get("/{project_id}/{user_id}/urls", status_code=status.HTTP_200_OK, response_model=list[UrlRead])
def read_user_urls(project_id: int, user_id: str, session: SessionDep, skip: int = 0, limit: int = 5):
    """Fetch urls assigned to a certain user in the project."""
    urls = project_crud.get_user_urls(session, project_id, user_id, skip=skip, limit=limit).all()
    return urls


@router.get("/{project_id}/urls", status_code=status.HTTP_200_OK, response_model=list[UrlRead])
def read_project_urls(project_id: int, session: SessionDep, skip: int = 0, limit: int = 5):
    """Fetch all urls assigned to a given project."""
    urls = project_crud.get_urls(session, project_id, skip=skip, limit=limit).all()
    return urls


@router.get("/{project_id}/users", status_code=status.HTTP_200_OK, response_model=list[UserRead])
def read_users(project_id: int, session: SessionDep):
    """Fetch all users assigned to a given project."""
    return users_crud.get_users_by_project(session, project_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProjectRead)
def create_project(project: ProjectCreateWithUsers, session: SessionDep):
    """Create a new project."""
    project_create = ProjectCreate.from_orm(project)
    created_project = project_crud.create_with_users(session, project_create, project.user_ids)
    return created_project


@router.put("/{project_id}")
def update_project(project_id: int):
    """Edit some properties of a project"""
    pass


@router.delete("/{project_id}")
def delete_project(project_id: int):
    """Delete a project."""
    pass
