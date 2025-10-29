import pytest
from unittest.mock import Mock

from service.category_service import CategoryService
from repository.category_repository import CategoryRepository
from mapper.category_mapper import CategoryMapper
from dto.category_dto import CategoryDto, CreateCategoryDto, UpdateCategoryDto
from exception.category_not_found_exception import CategoryNotFoundException

from tests.core.data.dto.category_factory import CategoryDTOFactory


@pytest.mark.unit
class TestCategoryServicePositive:
    """Тесты для CategoryService - проверяем бизнес-логику работы с категориями (Позитивыне проверки)"""

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        category_service: CategoryService,
        category_mock_mapper: CategoryMapper,
        category_mock_repository: CategoryRepository,
    ):
        """
        Тест успешного получения всех категорий
        Сценарий: В базе есть несколько категорий, сервис должен вернуть их DTO
        """
        CATEGORY_COUNT = 2
        expected_dto = CategoryDTOFactory.dto_list(count=CATEGORY_COUNT)
        orm_categories = [Mock(**dto.model_dump()) for dto in expected_dto]

        category_mock_repository.get_all.return_value = orm_categories
        category_mock_mapper.to_dto.side_effect = expected_dto

        result = await category_service.get_all()

        assert result == expected_dto
        category_mock_repository.get_all.assert_called_once()

        assert category_mock_mapper.to_dto.call_count == CATEGORY_COUNT
        category_mock_mapper.to_dto.assert_any_call(orm_model=orm_categories[0], dto_model=CategoryDto)

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        category_service: CategoryService,
        category_mock_mapper: CategoryMapper,
        category_mock_repository: CategoryRepository,
        sample_category_orm: dict,
        sample_category_dto: CategoryDto,
    ):
        """
        Тест успешного получения категории по ID
        Сценарий: Категория с указанным ID существует в базе
        """
        category_mock_repository.get_by_id.return_value = sample_category_orm
        category_mock_mapper.to_dto.return_value = sample_category_dto

        result = await category_service.get_by_id(1)

        assert result == sample_category_dto

        category_mock_repository.get_by_id.assert_called_once_with(1)
        category_mock_mapper.to_dto.assert_called_once_with(orm_model=sample_category_orm, dto_model=CategoryDto)

    @pytest.mark.asyncio
    async def test_create(
        self,
        category_service: CategoryService,
        category_mock_mapper: CategoryMapper,
        category_mock_repository: CategoryRepository,
        sample_category_orm: dict,
        sample_category_dto: CategoryDto,
        sample_create_category_dto: CreateCategoryDto,
    ):
        """
        Тест успешного создания категории
        Сценарий: Передаем DTO для создания, получаем созданную категорию как DTO
        """
        expected_dict = sample_create_category_dto.model_dump()
        category_mock_repository.create.return_value = sample_category_orm
        category_mock_mapper.to_dto.return_value = sample_category_dto
        category_mock_mapper.to_dict.return_value = expected_dict

        result = await category_service.create(dto=sample_create_category_dto)

        assert result == sample_category_dto
        category_mock_repository.create.assert_called_once_with(data=expected_dict)
        category_mock_mapper.to_dto.assert_called_once_with(orm_model=sample_category_orm, dto_model=CategoryDto)
        category_mock_mapper.to_dict.assert_called_once_with(dto_model=sample_create_category_dto)

    @pytest.mark.asyncio
    async def test_update(
        self,
        category_service: CategoryService,
        category_mock_mapper: CategoryMapper,
        category_mock_repository: CategoryRepository,
        sample_update_category_dto: UpdateCategoryDto,
    ):
        """
        Тест успешного обновления категории
        Сценарий: Обновляем данные категории по ID
        """
        expected_dict = sample_update_category_dto.model_dump()
        category_mock_mapper.to_dict.return_value = expected_dict

        await category_service.update(id=1, dto=sample_update_category_dto)

        category_mock_repository.update.assert_called_once_with(id=1, data=expected_dict)
        category_mock_mapper.to_dict.assert_called_once_with(dto_model=sample_update_category_dto)

    @pytest.mark.asyncio
    async def test_delete(
        self,
        category_service: CategoryService,
        category_mock_repository: CategoryRepository,
    ):
        """
        Тест успешного удаления категории
        Сценарий: Удаляем категорию по ID
        """
        await category_service.delete(id=1)
        category_mock_repository.delete.assert_called_once_with(id=1)


@pytest.mark.unit
class TestCategoryServiceNegative:
    """Тесты для CategoryService - проверяем бизнес-логику работы с категориями (Негативные проверки)"""

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        category_service: CategoryService,
        category_mock_repository: CategoryRepository,
    ):
        """
        Тест выброса исключения при получении несуществующей категории по ID
        Сценарий: Категория с указанным ID не существует в базе
        """
        category_mock_repository.get_by_id.return_value = None
        with pytest.raises(CategoryNotFoundException):
            await category_service.get_by_id(999)

        category_mock_repository.get_by_id.assert_called_once_with(999)
