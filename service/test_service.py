from typing import Callable
import inspect

from minio import S3Error

from repository.test_repository import TestRepository
from exception.test_env_is_not_load_exception import TestEnvIsNotLoadException
from settings import get_settings, TestInnerDockerSettings, TestSettings, settings

from utils.logger import logger


def is_testing_env() -> bool:
    current_settings = get_settings().__class__
    return current_settings == TestInnerDockerSettings or current_settings == TestSettings


def test_env_require(func: Callable):
    if inspect.iscoroutinefunction(func):

        async def wrapper(*args, **kwargs):
            if not is_testing_env():
                raise TestEnvIsNotLoadException
            return await func(*args, **kwargs)

    else:

        def wrapper(*args, **kwargs):
            if not is_testing_env():
                raise TestEnvIsNotLoadException
            return func(*args, **kwargs)

    return wrapper


class TestService:
    def __init__(self, repository: TestRepository):
        self.repository = repository

    @test_env_require
    def cleanup_minio(self) -> None:
        try:
            logger.info("Cleaning bucket after test")
            objects = settings.client.list_objects("files", recursive=True)
            for obj in objects:
                settings.client.remove_object("files", obj.object_name)
        except S3Error as e:
            logger.warning(f"Error cleaning bucket: {e}")

    @test_env_require
    async def cleanup_test_db(self) -> None:
        logger.info("Cleaning test database")
        await self.repository.cleanup_test_db()
        self.cleanup_minio()
