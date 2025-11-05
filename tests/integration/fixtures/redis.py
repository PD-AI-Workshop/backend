import pytest
from redis import Redis

from settings import settings


@pytest.fixture(scope="class")
def redis_client() -> Redis:
    client = settings.redis_client
    client.flushdb()
    return client
