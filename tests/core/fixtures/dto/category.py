import pytest

from dto.category_dto import CategoryDto, CreateCategoryDto, UpdateCategoryDto
from tests.core.data.dto.category_factory import CategoryDTOFactory


@pytest.fixture(scope="session")
def sample_category_dto() -> CategoryDto:
    return CategoryDTOFactory.dto()


@pytest.fixture(scope="session")
def sample_create_category_dto() -> CreateCategoryDto:
    return CategoryDTOFactory.create_dto()


@pytest.fixture(scope="session")
def sample_update_category_dto() -> UpdateCategoryDto:
    return CategoryDTOFactory.update_dto()
