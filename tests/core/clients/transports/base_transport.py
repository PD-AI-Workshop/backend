from httpx import AsyncClient
from typing import Optional

from tests.core.clients.http_client import HTTPClient
from tests.core.clients.auth_session import AuthSession


class BaseTransportClient(HTTPClient):
    def __init__(self, client: AsyncClient, auth: Optional[AuthSession]):
        super().__init__(client, auth)

    def _get_endpoint(self, *path) -> str:
        endpoint = self._endpoint
        if path:
            endpoint += "/".join(str(p) for p in path)
        return endpoint

    def _set_session(self, session: AuthSession):
        self._auth = session
