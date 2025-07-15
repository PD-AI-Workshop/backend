from fastapi import Depends
from enums.role import Role
from model.user import User
from auth.auth_router import fastapi_users
from exception.not_enough_permission_exception import NotEnoughPermissions


def role_required(required_roles: list[Role]):
    def dependency(user: User = Depends(fastapi_users.current_user())):

        if user.role not in required_roles:
            raise NotEnoughPermissions()

        return user

    return dependency


admin_dependency = [Depends(role_required([Role.ADMIN]))]

admin_and_writer_dependency = [Depends(role_required([Role.ADMIN, Role.WRITER]))]
