from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, **kwargs)


class UserExists(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=status.HTTP_409_CONFLICT, **kwargs)
