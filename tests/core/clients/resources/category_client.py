from typing import List

from tests.core.clients.transports.category_transport import CategoryTransportClient
from tests.core.clients.resources.base_client import BaseClient
from tests.core.schemas.resources.category_schema import (
    CreateCategoryRequestSchema,
    CreateCategoryResponseSchema,
    CategorySchema,
    GetCategoryResponseSchema,
    UpdateCategoryRequestSchema,
)
from tests.core.clients.auth_session import protected
from tests.core.utils.logger import get_logger
from tests.core.schemas.api_response import APIResponseSchema
from tests.core.clients.error_handler import error_handler


class CategoryClient(BaseClient):
    def __init__(self, transport: CategoryTransportClient):
        super().__init__(transport)
        self._logger = get_logger("Category client")

    @protected
    @error_handler('create category')
    async def create(self, data: CreateCategoryRequestSchema, **kwargs) -> APIResponseSchema[CreateCategoryResponseSchema]:
        response = await self._transport.create(json=data.model_dump(), **kwargs)
        response.raise_for_status()
        response_data = CreateCategoryResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @error_handler('get all categories')
    async def get_all(self, **kwargs) -> APIResponseSchema[List[CategorySchema]]:
        response = await self._transport.get_all(**kwargs)
        response.raise_for_status()
        response_data = [CategorySchema.model_validate(item) for item in response.json()]

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @error_handler('get category by id')
    async def get(self, id: int, **kwargs) -> APIResponseSchema[GetCategoryResponseSchema]:
        response = await self._transport.get_one(id=id, **kwargs)
        response.raise_for_status()
        response_data = GetCategoryResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @protected
    @error_handler('update category')
    async def update(self, id: int, data: UpdateCategoryRequestSchema, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.update(id=id, json=data.model_dump(), **kwargs)
        response.raise_for_status()

        return APIResponseSchema(status_code=response.status_code)

    @protected
    @error_handler('delete category')
    async def delete(self, id: int, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.delete(id=id, **kwargs)
        response.raise_for_status()

        return APIResponseSchema(status_code=response.status_code)
