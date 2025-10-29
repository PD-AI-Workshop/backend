import pytest
from redis import Redis
from unittest.mock import Mock

from model.user import User
from tests.core.data.fake_data_factory import fake_data_factory
from enums.role import Role


@pytest.fixture(scope="session")
def user() -> User:
    return User(
        id=fake_data_factory.ID(),
        username=fake_data_factory.username(),
        role=Role.USER,
        email=fake_data_factory.email(),
        is_active=False,
        is_superuser=False,
        is_verified=True,
    )


@pytest.fixture(scope="function")
def mock_redis_client() -> Redis:
    redis_mock = Mock()
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    return redis_mock
