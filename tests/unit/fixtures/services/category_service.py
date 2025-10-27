import pytest
from unittest.mock import Mock

from service.category_service import CategoryService
from repository.category_repository import CategoryRepository
from mapper.category_mapper import CategoryMapper


@pytest.fixture(scope="function")
def category_mock_mapper() -> Mock:
    return Mock(spec=CategoryMapper)

@pytest.fixture(scope="function")
def category_mock_repository() -> Mock:
    return Mock(spec=CategoryRepository)

@pytest.fixture(scope="function")
def category_mock_service(category_mock_mapper, category_mock_repository) -> CategoryService:
    return CategoryService(
        repository=category_mock_repository,
        mapper=category_mock_mapper
    )