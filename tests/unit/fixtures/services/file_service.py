import pytest
from unittest.mock import create_autospec

from service.file_service import FileService
from repository.file_repository import FileRepository
from repository.article_repository import ArticleRepository
from mapper.file_mapper import FileMapper
from dto.file_dto import FileDto


@pytest.fixture(scope="function")
def file_mock_mapper() -> FileMapper:
    return create_autospec(FileMapper)


@pytest.fixture(scope="function")
def file_mock_repository() -> FileRepository:
    return create_autospec(FileRepository)


@pytest.fixture(scope="function")
def file_service(
    file_mock_mapper: FileMapper, file_mock_repository: FileRepository, article_mock_repository: ArticleRepository
) -> FileService:
    return FileService(
        repository=file_mock_repository, mapper=file_mock_mapper, article_repository=article_mock_repository
    )


@pytest.fixture(scope="session")
def sample_file_orm(sample_file_dto: FileDto) -> dict:
    return sample_file_dto.model_dump()
