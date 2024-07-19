from typing import Optional

from fastapi import HTTPException, status


class CommonError(HTTPException):
    default_msg = "Bad request"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, error: Optional[str] = None, status_code: Optional[int] = None) -> None:
        if status_code is None:
            status_code = self.status_code
        if error is None:
            error = self.default_msg
        super().__init__(detail=error, status_code=status_code)


class EntityDoesNotExistError(CommonError):
    default_msg = "Entity not found"
    status_code = status.HTTP_404_NOT_FOUND
