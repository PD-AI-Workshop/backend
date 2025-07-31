from fastapi import APIRouter
from auth.auth_router import fastapi_users
from dto.user_dto import UpdateUserDTO, UserDTO
from repository.user_repository import repository
from dependencies.role_dependencies import admin_dependency

user_router = APIRouter()


@user_router.get("/", dependencies=admin_dependency)
async def get_all_users() -> list[UserDTO]:
    users = await repository.get_all_users()
    return [UserDTO.model_validate(user, from_attributes=True) for user in users]


user_router.include_router(fastapi_users.get_users_router(UserDTO, UpdateUserDTO))
