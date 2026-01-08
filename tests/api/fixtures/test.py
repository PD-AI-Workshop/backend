import pytest
from httpx import AsyncClient

from tests.core.clients.resources.test_client import TestClient
from tests.core.clients.auth_session import AuthSession

from tests.core.clients.transports.test_transport import TestTransportClient


@pytest.fixture(scope="function")
def _test_transport_client_private(httpx_client: AsyncClient, auth_session_admin: AuthSession) -> TestTransportClient:
    return TestTransportClient(client=httpx_client, auth=auth_session_admin)


@pytest.fixture(scope="function")
def test_client_private(_test_transport_client_private: TestTransportClient) -> TestClient:
    return TestClient(transport=_test_transport_client_private)
