import pytest

from repository.file_repository import FileRepository
from mapper.file_mapper import FileMapper
from service.file_service import FileService
from dto.file_dto import FileDto
from tests.core.data.dto.file_factory import FileDTOFactory
from exception.file_not_found_exception import FileNotFoundException


@pytest.mark.unit
class TestFileServicePositive:
    """Тесты для FileService - проверяем бизнес-логику работы с файлами (Позитивыне проверки)"""

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        file_service: FileService,
        file_mock_repository: FileRepository,
        file_mock_mapper: FileMapper,
    ):
        FILES_COUNT = 2
        sample_file_dto_list = FileDTOFactory.dto_list(count=FILES_COUNT)
        orm_files = [dto.model_dump() for dto in sample_file_dto_list]

        file_mock_repository.get_all.return_value = orm_files
        file_mock_mapper.to_dto.side_effect = sample_file_dto_list

        result = await file_service.get_all()

        assert result == sample_file_dto_list
        file_mock_repository.get_all.assert_called_once()
        file_mock_mapper.to_dto.call_count = FILES_COUNT

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        file_service: FileService,
        file_mock_repository: FileRepository,
        file_mock_mapper: FileMapper,
        sample_file_dto: FileDto,
        sample_file_orm: dict,
    ):
        file_mock_repository.get_by_id.return_value = sample_file_orm
        file_mock_mapper.to_dto.return_value = sample_file_dto

        result = await file_service.get_by_id(id=1)

        assert result == sample_file_dto
        file_mock_repository.get_by_id.assert_called_once_with(id=1)
        file_mock_mapper.to_dto.assert_called_once()


@pytest.mark.unit
class TestFileServiceNegative:
    """Тесты для FileService - проверяем бизнес-логику работы с файлами (Негативные проверки)"""

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        file_service: FileService,
        file_mock_repository: FileRepository,
        file_mock_mapper: FileMapper,
    ):
        file_mock_repository.get_by_id.return_value = None

        with pytest.raises(FileNotFoundException):
            await file_service.get_by_id(id=999)

        file_mock_repository.get_by_id.assert_called_once_with(id=999)
        assert file_mock_mapper.to_dto.call_count == 0
