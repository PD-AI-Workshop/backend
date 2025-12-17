from httpx import AsyncClient, Response
from typing import Optional

from tests.core.clients.transports.base_transport import BaseTransportClient
from tests.core.clients.auth_session import AuthSession
from tests.core.enums.endpoint import ResourceEndpoint


class AuthTransportClient(BaseTransportClient):
    def __init__(self, client: AsyncClient, auth: Optional[AuthSession] = None):
        super().__init__(client, auth)
        self._endpoint = ResourceEndpoint.AUTH

    async def register(self, json: dict, **kwargs) -> Response:
        endpoint = self._get_endpoint('register')
        return await self.post(endpoint=endpoint, json=json, **kwargs)

    async def login(self, data: dict, **kwargs) -> Response:
        endpoint = self._get_endpoint('login')
        return await self.post(endpoint=endpoint, data=data, **kwargs)
    
    async def logout(self, **kwargs) -> Response:
        endpoint = self._get_endpoint('logout')
        return await self.post(endpoint=endpoint, **kwargs)
