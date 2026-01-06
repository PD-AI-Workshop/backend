import pytest_asyncio

from tests.core.utils.logger import logger
from tests.core.clients.resources.test_client import TestClient


@pytest_asyncio.fixture(scope="function", autouse=True)
async def cleanup_test_db(test_client_private: TestClient):
    """Автоматическое отчищение базы для всех тестов"""
    yield
    logger.info("cleaning datebase up after test")
    await test_client_private.cleanup_test_db()
