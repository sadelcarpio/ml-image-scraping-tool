from fastapi import HTTPException, status


class ProjectNotFound(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, **kwargs)
