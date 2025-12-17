from httpx import Response
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

class CategoryClient(BaseClient):
    def __init__(self, transport: CategoryTransportClient):
        super().__init__(transport)

    @protected
    async def create(self, data: CreateCategoryRequestSchema, **kwargs) -> CreateCategoryResponseSchema:
        response = await self._transport.create(json=data.model_dump(), **kwargs)
        return CreateCategoryRequestSchema.model_validate_json(response.text)

    async def get_all(self, **kwargs) -> List[CategorySchema]:
        response = await self._transport.get_all(**kwargs)
        return [CategorySchema.model_validate(item) for item in response.json()]

    async def get(self, id: int, **kwargs) -> GetCategoryResponseSchema:
        response = await self._transport.get(id=id, **kwargs)
        return GetCategoryResponseSchema.model_validate_json(response.text)

    @protected
    async def update(self, id: int, data: UpdateCategoryRequestSchema, **kwargs) -> Response:
        return await self._transport.update(id=id, json=data.model_dump(), **kwargs)

    @protected
    async def delete(self, id: int, **kwargs) -> Response:
        return await self._transport.remove(id=id, **kwargs)
