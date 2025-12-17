from pydantic import BaseModel
from typing import Callable, ParamSpec, TypeVar
from functools import wraps

from tests.core.schemas.resources.user_schema import UserSchema


P = ParamSpec("P")
R = TypeVar("R")

def protected(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        kwargs["auth"] = True
        return func(*args, **kwargs)
    return wrapper


class LoggedInUserData(BaseModel):
    user: UserSchema
    token: str


class AuthSession:
    def __init__(self, credentials: LoggedInUserData):
        self.credentials = credentials

    @property
    def auth_headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self.credentials.token}'
        }