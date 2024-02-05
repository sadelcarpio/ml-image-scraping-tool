from fastapi import APIRouter

router = APIRouter(tags=["Users Endpoints"])


@router.get("/me")
def read_own_user():
    """Gets own user."""
    pass


@router.get("/me/project")
def read_own_user_projects():
    """Get the projects related to own user."""
    pass


@router.get("/{user_id}/projects")
def read_user_projects(user_id: int):
    """Get the projects related to a given user."""
    pass


@router.put("/me")
def update_own_user():
    """Edit own user."""
    pass


@router.delete("/me")
def delete_own_user():
    """Delete my current user."""
    pass
