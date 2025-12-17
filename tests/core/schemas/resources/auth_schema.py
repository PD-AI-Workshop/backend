from pydantic import Field

from tests.core.data.fake_data_factory import fake_data_factory
from tests.core.schemas.base import BaseSchema
from tests.core.enums.user_role import UserRole


class RegisterUserRequestSchema(BaseSchema):
    email: str = Field(default_factory=fake_data_factory.email)
    password: str = Field(default_factory=fake_data_factory.password)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    username: str = Field(default_factory=fake_data_factory.username)
    role: UserRole = UserRole.USER


class RegisterUserResponseSchema(BaseSchema):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    username: str
    role: UserRole


class LoginUserRequestSchema(BaseSchema):
    username: str
    password: str


class LoginUserResponseSchema(BaseSchema):
    access_token: str
    token_type: str
