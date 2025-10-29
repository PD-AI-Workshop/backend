import pytest
from unittest.mock import create_autospec

from service.category_service import CategoryService
from repository.category_repository import CategoryRepository
from mapper.category_mapper import CategoryMapper
from dto.category_dto import CategoryDto


@pytest.fixture(scope="function")
def category_mock_mapper() -> CategoryMapper:
    return create_autospec(CategoryMapper)


@pytest.fixture(scope="function")
def category_mock_repository() -> CategoryRepository:
    return create_autospec(CategoryRepository)


@pytest.fixture(scope="function")
def category_service(
    category_mock_mapper: CategoryMapper, category_mock_repository: CategoryRepository
) -> CategoryService:
    return CategoryService(repository=category_mock_repository, mapper=category_mock_mapper)


@pytest.fixture(scope="session")
def sample_category_orm(sample_category_dto: CategoryDto) -> dict:
    return sample_category_dto.model_dump()
