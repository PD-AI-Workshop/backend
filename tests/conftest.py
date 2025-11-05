import os
import pytest

from tests.core.utils.logger import logger

pytest_plugins = (
    "core.fixtures.dto.article",
    "core.fixtures.dto.file",
    "core.fixtures.dto.category",
)


def pytest_configure(config):
    os.environ["ENV"] = "TEST"


@pytest.fixture(autouse=True, scope="session")
def verify_test_environment():
    assert os.getenv("ENV") == "TEST", "non-test enviroment is active"
    logger.info("TEST enviroment is active")
    yield
