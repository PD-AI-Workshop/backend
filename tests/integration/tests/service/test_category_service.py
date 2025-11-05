import pytest

from service.category_service import CategoryService
from dto.category_dto import CategoryDto
from tests.core.data.dto.category_factory import CategoryDTOFactory
from exception.category_not_found_exception import CategoryNotFoundException


@pytest.mark.integration
class TestCategoryServiceIntegration:
    TARGET_ID = 1

    @pytest.mark.asyncio
    async def test_get_all(self, category_service: CategoryService):
        result = await category_service.get_all()

        assert len(result) > 0
        assert all(isinstance(item, CategoryDto) for item in result)

    @pytest.mark.asyncio
    async def test_get_by_id(self, category_service: CategoryService):
        result = await category_service.get_by_id(id=self.TARGET_ID)

        assert result.id == self.TARGET_ID
        assert isinstance(result, CategoryDto)

    @pytest.mark.asyncio
    async def test_create(self, category_service: CategoryService):
        data = CategoryDTOFactory.create_dto()
        result = await category_service.create(dto=data)

        assert isinstance(result, CategoryDto)
        assert result.name == data.name

    @pytest.mark.asyncio
    async def test_update(self, category_service: CategoryService):
        data = CategoryDTOFactory.update_dto()
        await category_service.update(id=self.TARGET_ID, dto=data)
        result = await category_service.get_by_id(id=self.TARGET_ID)

        assert result.name == data.name

    @pytest.mark.asyncio
    async def test_delete(self, category_service: CategoryService):
        await category_service.delete(id=self.TARGET_ID)

        with pytest.raises(CategoryNotFoundException):
            await category_service.get_by_id(id=self.TARGET_ID)
