from fastapi import APIRouter, status, Security
from sqlmodel import select

from app.api.deps import SessionDep
from app.crud.crud_project import CRUDProjectDep
from app.crud.crud_user import CRUDUserDep
from app.exceptions.projects import ProjectNotFound, ProjectExists, InvalidTaskType
from app.exceptions.users import UserNotFound, UserExists
from app.models.projects import ProjectModel
from app.models.urls import UrlModel
from app.models.users import UserModel
from app.schemas.extras import TaskType
from app.schemas.projects import ProjectRead, ProjectCreateWithUsers, ProjectUpdate, ProjectReadWithUsers
from app.schemas.urls import UrlRead
from app.schemas.users import UserRead
from app.security.auth import CurrentAdminUser, get_current_user

router = APIRouter(tags=["Projects Endpoints"], dependencies=[Security(get_current_user, scopes=["admin"])])


@router.get("/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectRead)
def project_information(project_id: int, projects_crud: CRUDProjectDep) -> ProjectModel:
    """Fetch information from a certain project."""
    project = projects_crud.get(project_id)
    if project is None:
        raise ProjectNotFound(detail=f"No such project with id: {project_id}")
    return project


@router.get("/{project_id}/{user_id}/urls", status_code=status.HTTP_200_OK, response_model=list[UrlRead])
def read_user_urls(project_id: int,
                   user_id: str,
                   projects_crud: CRUDProjectDep,
                   skip: int = 0,
                   limit: int = 5) -> list[UrlModel]:
    """Fetch urls assigned to a certain user in the project."""
    urls = projects_crud.get_user_urls(project_id, user_id, skip=skip, limit=limit).all()
    return urls


@router.get("/{project_id}/urls", status_code=status.HTTP_200_OK, response_model=list[UrlRead])
def read_project_urls(project_id: int,
                      projects_crud: CRUDProjectDep,
                      skip: int = 0,
                      limit: int = 5) -> list[UrlModel]:
    """Fetch all urls assigned to a given project."""
    urls = projects_crud.get_urls(project_id, skip=skip, limit=limit).all()
    return urls


@router.get("/{project_id}/users", status_code=status.HTTP_200_OK, response_model=list[UserRead])
def read_users(project_id: int,
               projects_crud: CRUDProjectDep,
               skip: int = 0,
               limit: int = 5) -> list[UserModel]:
    """Fetch all users assigned to a given project."""
    users = projects_crud.get_users_by_project(project_id, skip=skip, limit=limit).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProjectReadWithUsers)
def create_project(project: ProjectCreateWithUsers,
                   session: SessionDep,
                   current_admin_user: CurrentAdminUser,
                   projects_crud: CRUDProjectDep) -> ProjectModel:
    """Create a new project."""
    dup_project = session.exec(select(ProjectModel).where(ProjectModel.name == project.name)).first()
    if dup_project is not None:
        raise ProjectExists(detail=f"A project with this name already exists.")
    for e in TaskType:
        if e.value == project.task_type:
            break
    else:
        raise InvalidTaskType()
    created_project = projects_crud.create_with_users(project, current_admin_user.id)
    return created_project


@router.put("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_project(project_id: int,
                   current_admin_user: CurrentAdminUser,
                   project_updates: ProjectUpdate,
                   projects_crud: CRUDProjectDep):
    """Edit some properties of a project"""
    project_to_update = projects_crud.get(project_id)
    if project_to_update is None:
        raise ProjectNotFound(detail=f"No such project with id: {project_id}")
    for owned_project in current_admin_user.projects_owned:
        if owned_project.id == project_id:
            break
    else:
        raise ProjectNotFound(detail=f"Project not in user's owned projects.")
    projects_crud.update(project_to_update, project_updates)


@router.put("/{project_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_user(project_id: int,
             user_id: str,
             current_admin_user: CurrentAdminUser,
             projects_crud: CRUDProjectDep,
             users_crud: CRUDUserDep):
    """Add a user to the project"""
    project = projects_crud.get(project_id)
    if project is None:
        raise ProjectNotFound(detail=f"No such project with id: {project_id}")
    for owned_project in current_admin_user.projects_owned:
        if owned_project.id == project_id:
            break
    else:
        raise ProjectNotFound(detail=f"Project not in user's owned projects.")
    user = users_crud.get(user_id)
    if user is None:
        raise UserNotFound(detail=f"No user found with id: {user_id}")
    for project_user in project.users:
        if str(project_user.id) == user_id:
            raise UserExists(detail=f"User is already in the project.")
    projects_crud.add_user(project, user)


@router.delete("/{project_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(project_id: int,
                user_id: str,
                current_admin_user: CurrentAdminUser,
                projects_crud: CRUDProjectDep,
                users_crud: CRUDUserDep):
    """Remove a user from the project"""
    project = projects_crud.get(project_id)
    if project is None:
        raise ProjectNotFound(detail=f"No such project with id: {project_id}")
    for owned_project in current_admin_user.projects_owned:
        if owned_project.id == project_id:
            break
    else:
        raise ProjectNotFound(detail=f"Project not in user's owned projects.")
    user = users_crud.get(user_id)
    if user is None:
        raise UserNotFound(detail=f"No user found with id: {user_id}")
    for project_user in project.users:
        if str(project_user.id) == user_id:
            break
    else:
        raise UserNotFound(detail=f"User not in project")
    projects_crud.remove_user(project, user)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, current_admin_user: CurrentAdminUser, projects_crud: CRUDProjectDep):
    """Delete a project."""
    project = projects_crud.get(project_id)
    if project is None:
        raise ProjectNotFound(detail=f"No such project with id: {project_id}")
    for owned_project in current_admin_user.projects_owned:
        if owned_project.id == project_id:
            break
    else:
        raise ProjectNotFound(detail=f"Project not in user's owned projects.")
    projects_crud.remove(project)
