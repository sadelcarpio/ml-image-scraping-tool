from fastapi import HTTPException, status

from app.schemas.extras import TaskType


class ProjectNotFound(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, **kwargs)


class ProjectExists(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=status.HTTP_409_CONFLICT, **kwargs)


class InvalidTaskType(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Invalid task_type field, please select a "
                                f"valid task field from {[e.value for e in TaskType]}")
