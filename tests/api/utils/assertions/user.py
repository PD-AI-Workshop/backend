from http import HTTPStatus
from typing import List

from tests.api.utils.assertions.base import assert_equal, assert_status_code, assert_length
from tests.core.schemas.resources.user_schema import (
    UserSchema,
    GetUserResponseSchema,
    UpdateUserRequestSchema,
    UpdateUserResponseSchema,
    UserWithPasswordSchema
)
from tests.core.schemas.api_response import APIResponseSchema


def assert_get_all_response(response: APIResponseSchema[List[UserSchema]], users: List[UserWithPasswordSchema]):
    assert_status_code(response.status_code, HTTPStatus.OK)
    # + 1 так как мы дополнительно создали админа для получения всех созданных в тесте пользователей
    assert_length(response.data, len(users) + 1, 'users count')


def assert_get_by_id_response(response: APIResponseSchema[GetUserResponseSchema], user: UserWithPasswordSchema):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal(response.data.id, user.id, 'ID')
    assert_equal(response.data.email, user.email, 'email')
    assert_equal(response.data.is_active, user.is_active, 'is_active')
    assert_equal(response.data.is_superuser, user.is_superuser, 'is_superuser')
    assert_equal(response.data.is_verified, user.is_verified, 'is_verified')
    assert_equal(response.data.username, user.username, 'username')
    assert_equal(response.data.role, user.role, 'role')


def assert_get_current_user_response(response: APIResponseSchema[GetUserResponseSchema], user: UserWithPasswordSchema):
    assert_get_by_id_response(response, user)


def assert_update_by_id_response(response: APIResponseSchema[UpdateUserResponseSchema], request: UpdateUserRequestSchema):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal(response.data.email, request.email, 'email')
    assert_equal(response.data.is_active, request.is_active, 'is_active')
    assert_equal(response.data.is_superuser, request.is_superuser, 'is_superuser')
    assert_equal(response.data.is_verified, request.is_verified, 'is_verified')
    assert_equal(response.data.username, request.username, 'username')
    assert_equal(response.data.role, request.role, 'role')


def assert_update_current_user_response(response: APIResponseSchema[UpdateUserResponseSchema], request: UpdateUserRequestSchema):
    assert_update_by_id_response(response, request)


def assert_delete_by_id_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.NO_CONTENT)
