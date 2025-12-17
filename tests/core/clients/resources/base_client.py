from tests.core.clients.transports.base_transport import BaseTransportClient
from tests.core.clients.auth_session import AuthSession
from tests.core.schemas.api_response import APIResponseSchema


class BaseClient:
    def __init__(self, transport: BaseTransportClient):
        self._transport = transport

    @staticmethod
    def _create_error_response(message: str, status_code: int) -> APIResponseSchema[None]:
        return APIResponseSchema.create_error(message, status_code=status_code)

    def make_private(self, session: AuthSession):
        self._transport._set_session(session)