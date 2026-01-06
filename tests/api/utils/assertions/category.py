from http import HTTPStatus
from typing import List

from tests.api.utils.assertions.base import assert_equal, assert_status_code, assert_equal_length
from tests.core.schemas.resources.category_schema import (
    CategorySchema, 
    GetCategoryResponseSchema,
    CreateCategoryResponseSchema,
    CreateCategoryRequestSchema,
)
from tests.core.schemas.api_response import APIResponseSchema


def assert_get_all_response(response: APIResponseSchema[List[CategorySchema]], categories: List[CategorySchema]):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal_length(response.data, categories, 'categories count')


def assert_get_by_id_response(response: APIResponseSchema[GetCategoryResponseSchema], category: CategorySchema):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal(response.data.id, category.id, 'ID')
    assert_equal(response.data.name, category.name, 'name')


def assert_create_response(response: APIResponseSchema[CreateCategoryResponseSchema], request: CreateCategoryRequestSchema):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal(response.data.name, request.name, 'name')


def assert_update_by_id_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.OK)


def assert_delete_by_id_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.OK)
