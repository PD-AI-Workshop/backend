from typing import Generic, TypeVar, Optional
from pydantic import BaseModel


T = TypeVar("T")


class APIResponseSchema(BaseModel, Generic[T]):
    success: bool = True
    response: Optional[T] = None
    status_code: int = 200
    message: Optional[str] = None

    @classmethod
    def create_success(cls, response: T = None, status_code: int = 200) -> "APIResponseSchema[T]":
        return cls(response=response, status_code=status_code)

    @classmethod
    def create_error(cls, message: str, status_code: int = 400) -> "APIResponseSchema[None]":
        return cls(success=False, response=None, status_code=status_code, message=message)
