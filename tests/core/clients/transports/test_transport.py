from typing import Optional
from httpx import AsyncClient, Response

from tests.core.clients.auth_session import AuthSession
from tests.core.clients.transports.base_transport import BaseTransportClient
from tests.core.enums.endpoint import ResourceEndpoint


class TestTransportClient(BaseTransportClient):
    def __init__(self, client: AsyncClient, auth: Optional[AuthSession] = None):
        super().__init__(client, auth)
        self._endpoint = ResourceEndpoint.TEST

    async def cleanup_test_db(self, **kwargs) -> Response:
        endpoint = self._get_endpoint("database")
        return await self.delete(endpoint=endpoint, **kwargs)
