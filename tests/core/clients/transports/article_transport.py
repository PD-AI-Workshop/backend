from typing import Optional
from httpx import AsyncClient, Response

from tests.core.clients.auth_session import AuthSession
from tests.core.clients.transports.base_transport import BaseTransportClient
from tests.core.enums.endpoint import ResourceEndpoint


class ArticleTransportClient(BaseTransportClient):
    def __init__(self, client: AsyncClient, auth: Optional[AuthSession] = None):
        super().__init__(client, auth)
        self._endpoint = ResourceEndpoint.ARTICLE

    async def create(self, json: dict, **kwargs) -> Response:
        endpoint = self._get_endpoint()
        return await self.post(endpoint=endpoint, json=json, **kwargs)

    async def get_all(self, **kwargs) -> Response:
        endpoint = self._get_endpoint()
        return await super().get(endpoint=endpoint, **kwargs)

    async def get_one(self, id: int, **kwargs) -> Response:
        endpoint = self._get_endpoint(id)
        return await super().get(endpoint=endpoint, **kwargs)

    async def update(self, id: int, json: dict, **kwargs) -> Response:
        endpoint = self._get_endpoint(id)
        return await self.put(endpoint=endpoint, json=json, **kwargs)

    async def delete(self, id: int, **kwargs) -> Response:
        endpoint = self._get_endpoint(id)
        return await super().delete(endpoint=endpoint, **kwargs)
