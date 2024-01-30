from fastapi import APIRouter

from app.api.deps import SessionDep
from app.crud import CRUDProject
from app.models.projects import ProjectModel
from app.schemas.projects import ProjectRead
from app.schemas.urls import UrlRead

router = APIRouter(tags=["Projects Endpoints"])
project = CRUDProject(ProjectModel)


@router.get("/{project_id}", response_model=ProjectRead)
def project_information(project_id: int, session: SessionDep):
    """Fetch information from a certain project."""
    return project.get(session, project_id)


@router.get("/{project_id}/{user_id}/urls")
def read_user_urls(project_id: int, user_id: str, session: SessionDep, skip: int = 0, limit: int = 5):
    """Fetch urls assigned to a certain user in the project."""
    urls = project.get_urls(session, project_id, skip=skip, limit=limit).all()
    return urls


@router.get("/{project_id}/urls", response_model=list[UrlRead])
def read_project_urls(project_id: int, session: SessionDep, skip: int = 0, limit: int = 5):
    """Fetch all urls assigned to a given project."""
    urls = project.get_urls(session, project_id, skip=skip, limit=limit).all()
    return urls


@router.get("/{project_id}/users")
def read_users(project_id: int):
    """Fetch all users assigned to a given project."""
    pass


@router.post("/")
def create_project():
    """Create a new project."""
    pass


@router.put("/{project_id}")
def update_project(project_id: int):
    """Edit some properties of a project"""
    pass


@router.delete("/{project_id}")
def delete_project(project_id: int):
    """Delete a project."""
    pass
