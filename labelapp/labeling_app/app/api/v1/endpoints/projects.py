from fastapi import APIRouter

router = APIRouter(tags=["Projects Endpoints"])


@router.get("/{project_id}")
def project_information(project_id: int):
    """Fetch information from a certain project."""
    pass


@router.get("/{project_id}/{user_id}/urls")
def read_user_urls(project_id: int, user_id: int):
    """Fetch urls assigned to a certain user in the project."""
    pass


@router.get("/{project_id}/urls")
def read_project_urls(project_id: int):
    """Fetch all urls assigned to a given project."""
    pass


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
