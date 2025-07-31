from typing import Optional
from enums.role import Role
from fastapi_users import schemas


class UserDTO(schemas.BaseUser[int]):
    username: str
    role: Role


class CreateUserDTO(schemas.BaseUserCreate):
    username: str
    role: Role


class UpdateUserDTO(schemas.BaseUserUpdate):
    username: Optional[str] = None
    role: Optional[Role] = None
