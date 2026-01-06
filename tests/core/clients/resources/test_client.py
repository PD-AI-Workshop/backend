from tests.core.clients.transports.test_transport import TestTransportClient
from tests.core.clients.resources.base_client import BaseClient
from tests.core.clients.auth_session import protected
from tests.core.utils.logger import get_logger
from tests.core.schemas.api_response import APIResponseSchema
from tests.core.clients.error_handler import error_handler


class TestClient(BaseClient):
    def __init__(self, transport: TestTransportClient):
        super().__init__(transport)
        self._logger = get_logger("Test client")

    @protected
    @error_handler('cleanup test database')
    async def cleanup_test_db(self, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.cleanup_test_db(**kwargs)
        response.raise_for_status()

        return APIResponseSchema(status_code=response.status_code)
