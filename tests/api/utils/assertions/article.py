from http import HTTPStatus
from typing import List

from tests.api.utils.assertions.base import assert_equal, assert_status_code, assert_equal_length, assert_is_false
from tests.core.schemas.resources.article_schema import (
    ArticleSchema,
    CreateArticleRequestSchema,
    CreateArticleResponseSchema,
    GetArticleResponseSchema,
)
from tests.core.schemas.api_response import APIResponseSchema


def assert_get_all_response(response: APIResponseSchema[List[ArticleSchema]], articles: List[ArticleSchema]):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal_length(response.data, articles, "articles count")


def assert_get_by_id_response(response: APIResponseSchema[GetArticleResponseSchema], article: ArticleSchema):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal(response.data.id, article.id, "ID")
    assert_equal(response.data.title, article.title, "title")
    assert_equal(response.data.created_date, article.created_date, "created_date")
    assert_equal(response.data.time_reading, article.time_reading, "time_reading")
    assert_equal(response.data.main_image_url, article.main_image_url, "main_image_url")
    assert_equal(response.data.text_id, article.text_id, "text_id")
    assert_equal(response.data.user_id, article.user_id, "user_id")
    assert_equal(response.data.username, article.username, "username")
    assert_equal(response.data.category_ids, article.category_ids, "category_ids")
    assert_equal(response.data.image_ids, article.image_ids, "image_ids")


def assert_create_response(
    response: APIResponseSchema[CreateArticleResponseSchema], request: CreateArticleRequestSchema
):
    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_equal(response.data.title, request.title, "title")
    assert_equal(response.data.time_reading, request.time_reading, "time_reading")
    assert_equal(response.data.main_image_url, request.main_image_url, "main_image_url")
    assert_equal(response.data.text_id, request.text_id, "text_id")
    assert_equal(response.data.category_ids, request.category_ids, "category_ids")
    assert_equal(response.data.image_ids, request.image_ids, "image_ids")


def assert_update_by_id_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.OK)


def assert_delete_by_id_response(response: APIResponseSchema[None]):
    assert_status_code(response.status_code, HTTPStatus.OK)


def assert_get_by_id_not_found_response(response: APIResponseSchema[GetArticleResponseSchema]):
    assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
    assert_is_false(response.data, "article_data")
