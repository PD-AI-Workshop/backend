from typing import Optional
from enums.role import Role
from fastapi_users import schemas


class UserDTO(schemas.BaseUser[int]):
    image_url: str
    role: Role


class CreateUserDTO(schemas.BaseUserCreate):
    image_url: Optional[str] = None
    role: Role


class UpdateUserDTO(schemas.BaseUserUpdate):
    image_url: Optional[str] = None
    role: Role
