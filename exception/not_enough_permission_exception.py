from fastapi import HTTPException


class NotEnoughPermissions(HTTPException):
    status_code = 403
    detail = "Not enough permissions"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
