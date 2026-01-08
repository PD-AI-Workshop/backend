from http import HTTPStatus
from typing import List

from tests.api.utils.assertions.base import assert_equal, assert_status_code, assert_equal_length, assert_is_true
from tests.core.schemas.resources.file_schema import (
    FileSchema,
    GetFileResponseSchema,
    CreateFileResponseSchema,
)
from tests.core.schemas.api_response import APIResponseSchema


def assert_get_all_response(response: APIResponseSchema[List[FileSchema]], files: List[FileSchema]):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal_length(response.data, files, "files count")


def assert_get_by_id_response(response: APIResponseSchema[GetFileResponseSchema], file: FileSchema):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal(response.data.id, file.id, "ID")
    assert_equal(response.data.name, file.name, "name")
    assert_equal(response.data.size, file.size, "size")
    assert_equal(response.data.url, file.url, "url")


def assert_get_by_filename_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_is_true(response.binary_data, "binary data of file")


def assert_create_response(response: APIResponseSchema[CreateFileResponseSchema]):
    assert_status_code(response.status_code, HTTPStatus.OK)


def assert_update_by_id_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.OK)


def assert_delete_by_id_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.OK)


def assert_delete_unused_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.OK)
