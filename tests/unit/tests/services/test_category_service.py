import pytest
from typing import cast
from unittest.mock import Mock

from service.category_service import CategoryService
from repository.category_repository import CategoryRepository
from mapper.category_mapper import CategoryMapper
from dto.category_dto import CategoryDto


@pytest.mark.unit
class TestCategoryService:
    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self,
        category_mock_service: CategoryService, 
        category_mock_mapper: Mock,
        category_mock_repository: Mock
    ):
        repo = cast(CategoryRepository, category_mock_repository)
        mapper = cast(CategoryMapper, category_mock_mapper)

        orm_category = Mock(id=1, name="Test Category")
        expected_dto = CategoryDto(id=1, name="Test Category")

        repo.get_by_id.return_value = orm_category
        mapper.to_dto.return_value = expected_dto

        result = await category_mock_service.get_by_id(1)

        assert result == expected_dto

        repo.get_by_id.assert_called_once_with(1)
        mapper.to_dto.assert_called_once_with(
            orm_model=orm_category, 
            dto_model=CategoryDto
        )
        
