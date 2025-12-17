from typing import Optional
from httpx import AsyncClient, Response

from tests.core.clients.auth_session import AuthSession
from tests.core.clients.transports.base_transport import BaseTransportClient
from tests.core.enums.endpoint import ResourceEndpoint


class UserTransportClient(BaseTransportClient):
    def __init__(self, client: AsyncClient, auth: Optional[AuthSession] = None):
        super().__init__(client, auth)
        self._endpoint = ResourceEndpoint.USER

    async def get_all(self, **kwargs) -> Response:
        endpoint = self._get_endpoint()
        return await self.get(endpoint=endpoint, **kwargs)

    async def get(self, id: int, **kwargs) -> Response:
        endpoint = self._get_endpoint(id)
        return await super().get(endpoint=endpoint, **kwargs)

    async def get_me(self, **kwargs) -> Response:
        endpoint = self._get_endpoint("me")
        return await super().get(endpoint=endpoint, **kwargs)

    async def update(self, id: int, json: dict, **kwargs) -> Response:
        endpoint = self._get_endpoint(id)
        return await self.patch(endpoint=endpoint, json=json, **kwargs)

    async def update_me(self, json: dict, **kwargs) -> Response:
        endpoint = self._get_endpoint("me")
        return await self.patch(endpoint=endpoint, json=json, **kwargs)

    async def remove(self, **kwargs) -> Response:
        endpoint = self._get_endpoint(id)
        return await self.delete(endpoint=endpoint, **kwargs)
