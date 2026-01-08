import pytest
from httpx import AsyncClient

from tests.core.clients.event_hooks import log_response_event_hook, log_request_event_hook
from tests.config import settings


pytest_plugins = (
    "fixtures.db",
    "fixtures.auth",
    "fixtures.user",
    "fixtures.test",
    "fixtures.category",
    "fixtures.file",
    "fixtures.article",
)


@pytest.fixture(scope="function")
def httpx_client() -> AsyncClient:
    return AsyncClient(
        base_url=settings.API_BASE_URL,
        timeout=settings.TIMEOUT,
        event_hooks={
            "request": [log_request_event_hook],
            "response": [log_response_event_hook],
        },
    )


@pytest.fixture(scope="function")
async def cleanup_client(httpx_client: AsyncClient):
    yield
    await httpx_client.aclose()
