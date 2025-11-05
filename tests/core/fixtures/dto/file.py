import pytest

from dto.file_dto import FileDto
from tests.core.data.dto.file_factory import FileDTOFactory


@pytest.fixture(scope="session")
def sample_file_dto() -> FileDto:
    return FileDTOFactory.dto()
