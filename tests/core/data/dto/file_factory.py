from dto.file_dto import FileDto
from tests.core.data.dto.base_factory import BaseDTOFactory
from tests.core.data.fake_data_factory import fake_data_factory


class FileDTOFactory(BaseDTOFactory[FileDto]):
    @classmethod
    def dto(cls, **overrides) -> FileDto:
        defaults = {
            "id": fake_data_factory.ID(),
            "name": fake_data_factory.title(),
            "size": fake_data_factory.integer(),
            "url": fake_data_factory.url(),
        }
        defaults.update(overrides)
        return FileDto(**defaults)
