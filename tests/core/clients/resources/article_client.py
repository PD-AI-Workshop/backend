from typing import List

from tests.core.clients.transports.article_transport import ArticleTransportClient
from tests.core.clients.resources.base_client import BaseClient
from tests.core.schemas.resources.article_schema import (
    ArticleSchema,
    CreateArticleRequestSchema,
    CreateArticleResponseSchema,
    GetArticleResponseSchema,
    UpdateArticleRequestSchema,
)
from tests.core.clients.auth_session import protected
from tests.core.utils.logger import get_logger
from tests.core.schemas.api_response import APIResponseSchema
from tests.core.clients.error_handler import error_handler
from tests.api.utils.assertions.json_schema import validate_json_schema


class ArticleClient(BaseClient):
    def __init__(self, transport: ArticleTransportClient):
        super().__init__(transport)
        self._logger = get_logger("ARTICLE CLIENT")

    @protected
    @error_handler("create article")
    async def create(
        self, data: CreateArticleRequestSchema, **kwargs
    ) -> APIResponseSchema[CreateArticleResponseSchema]:
        response = await self._transport.create(json=data.model_dump(), **kwargs)
        response.raise_for_status()
        validate_json_schema(response.json(), CreateArticleResponseSchema.model_json_schema())
        response_data = CreateArticleResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @error_handler("get all articles")
    async def get_all(self, **kwargs) -> APIResponseSchema[List[ArticleSchema]]:
        response = await self._transport.get_all(**kwargs)
        response.raise_for_status()

        for item in response.json():
            validate_json_schema(item, ArticleSchema.model_json_schema())

        response_data = [ArticleSchema.model_validate(item) for item in response.json()]

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @error_handler("get article by id")
    async def get(self, id: int, **kwargs) -> APIResponseSchema[GetArticleResponseSchema]:
        response = await self._transport.get_one(id=id, **kwargs)
        response.raise_for_status()
        validate_json_schema(response.json(), GetArticleResponseSchema.model_json_schema())
        response_data = GetArticleResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @protected
    @error_handler("update article by id")
    async def update(self, id: int, data: UpdateArticleRequestSchema, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.update(id=id, json=data.model_dump(), **kwargs)
        response.raise_for_status()

        return APIResponseSchema(status_code=response.status_code)

    @protected
    @error_handler("delete article by id")
    async def delete(self, id: int, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.delete(id=id, **kwargs)
        response.raise_for_status()

        return APIResponseSchema(status_code=response.status_code)
