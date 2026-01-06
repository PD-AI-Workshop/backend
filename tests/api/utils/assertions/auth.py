from http import HTTPStatus

from tests.api.utils.assertions.base import assert_equal, assert_status_code, assert_is_true
from tests.core.schemas.resources.auth_schema import RegisterUserResponseSchema, RegisterUserRequestSchema, LoginUserResponseSchema
from tests.core.schemas.api_response import APIResponseSchema


def assert_register_response(response: APIResponseSchema[RegisterUserResponseSchema], request: RegisterUserRequestSchema):
    assert_status_code(response.status_code, HTTPStatus.CREATED)
    assert_equal(response.data.email, request.email, 'email')
    assert_equal(response.data.is_active, request.is_active, 'is_active')
    assert_equal(response.data.is_superuser, request.is_superuser, 'is_superuser')
    assert_equal(response.data.is_verified, request.is_verified, 'is_verified')
    assert_equal(response.data.username, request.username, 'username')
    assert_equal(response.data.role, request.role, 'role')

def assert_login_response(response: APIResponseSchema[LoginUserResponseSchema]):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_is_true(response.data.access_token, 'access_token')
    assert_equal(response.data.token_type, 'bearer', 'token_type')

def assert_logout_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.NO_CONTENT)
