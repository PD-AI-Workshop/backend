from pydantic import Field

from tests.core.schemas.base import BaseSchema
from tests.core.enums.user_role import UserRole
from tests.core.data.fake_data_factory import fake_data_factory


class UserSchema(BaseSchema):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    username: str
    role: UserRole


class UserWithPasswordSchema(UserSchema):
    password: str


class GetUserResponseSchema(UserSchema):
    pass


class UpdateUserRequestSchema(BaseSchema):
    password: str = Field(default_factory=fake_data_factory.password)
    email: str = Field(default_factory=fake_data_factory.email)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    username: str = Field(default_factory=fake_data_factory.username)
    role: UserRole = UserRole.USER


class UpdateUserResponseSchema(UserSchema):
    pass
