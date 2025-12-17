from typing import Optional
from httpx import AsyncClient, Response

from tests.core.clients.auth_session import AuthSession
from tests.core.clients.transports.base_transport import BaseTransportClient
from tests.core.enums.endpoint import ResourceEndpoint


class CategoryTransportClient(BaseTransportClient):
    def __init__(self, client: AsyncClient, auth: Optional[AuthSession] = None):
        super().__init__(client, auth)
        self._endpoint = ResourceEndpoint.CATEGORY

    async def create(self, json: dict, **kwargs) -> Response:
        endpoint = self._get_endpoint()
        return await self.post(endpoint=endpoint, json=json, **kwargs)

    async def get_all(self, **kwargs) -> Response:
        endpoint = self._get_endpoint()
        return await self.get(endpoint=endpoint, **kwargs)

    async def get(self, id: int, params: dict | None = None, **kwargs) -> Response:
        endpoint = self._get_endpoint(id)
        return await self.get(endpoint=endpoint, params=params, **kwargs)

    async def update(self, id: int, json: dict, **kwargs) -> Response:
        endpoint = self._get_endpoint(id)
        return await self.put(endpoint=endpoint, json=json, **kwargs)

    async def remove(self, **kwargs) -> Response:
        endpoint = self._get_endpoint(id)
        return await self.delete(endpoint=endpoint, **kwargs)
