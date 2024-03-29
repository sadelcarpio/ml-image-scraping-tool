from fastapi import APIRouter
from fastapi import status
from sqlmodel import select

from app.api.deps import SessionDep
from app.crud.crud_user import CRUDUserDep
from app.exceptions.users import UserExists
from app.models.projects import ProjectModel
from app.models.users import UserModel
from app.schemas.projects import ProjectRead
from app.schemas.users import UserUpdate, UserRead, UserCreate
from app.security.auth import CurrentUser, CurrentAdminUser

router = APIRouter(tags=["Users Endpoints"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserRead)
def read_own_user(current_user: CurrentUser) -> UserModel:
    """Gets own user."""
    return current_user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def create_user(user: UserCreate, session: SessionDep, users_crud: CRUDUserDep) -> UserModel:
    """Creates a new user"""
    dup_user = session.exec(select(UserModel).where((UserModel.username == user.username) |
                                                    (UserModel.email == user.email))).first()
    if dup_user is not None:
        raise UserExists(detail="A user already exists with this username or email.")
    created_user = users_crud.create_with_pwd_hashing(user)
    return created_user


@router.get("/me/projects-owned", status_code=status.HTTP_200_OK, response_model=list[ProjectRead])
def read_own_user_projects_owned(
        current_user: CurrentAdminUser,
        users_crud: CRUDUserDep,
        skip: int = 0,
        limit: int = 5) -> list[ProjectModel]:
    """Get the projects owned by own user."""
    projects = users_crud.get_projects_by_owner(current_user.id, skip=skip, limit=limit).all()
    return projects


@router.get("/me/projects", status_code=status.HTTP_200_OK, response_model=list[ProjectRead])
def read_own_user_projects(
        current_user: CurrentUser,
        users_crud: CRUDUserDep,
        skip: int = 0,
        limit: int = 5) -> list[ProjectModel]:
    """Get the projects assigned to own user."""
    projects = users_crud.get_assigned_projects(current_user.id, skip=skip, limit=limit).all()
    return projects


@router.get("/{user_id}/projects", status_code=status.HTTP_200_OK, response_model=list[ProjectRead])
def read_user_projects(
        user_id: str,
        users_crud: CRUDUserDep,
        current_user: CurrentAdminUser,
        skip: int = 0,
        limit: int = 5) -> list[ProjectModel]:
    """Get the projects assigned to a given user."""
    projects = users_crud.get_assigned_projects(user_id, skip=skip, limit=limit).all()
    return projects


@router.put("/me", status_code=status.HTTP_204_NO_CONTENT)
def update_own_user(current_user: CurrentUser, users_crud: CRUDUserDep, to_update: UserUpdate):
    """Edit own user."""
    users_crud.update(current_user, to_update)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_own_user(current_user: CurrentUser, users_crud: CRUDUserDep):
    """Delete my current user."""
    users_crud.remove(current_user)
