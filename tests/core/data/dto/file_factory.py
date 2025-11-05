from dto.file_dto import FileDto, CreateFileDto, UpdateFileDto
from tests.core.data.dto.base_factory import BaseDTOFactory
from tests.core.data.fake_data_factory import fake_data_factory


class FileDTOFactory(BaseDTOFactory[FileDto]):
    @classmethod
    def dto(cls, to_dict: bool = False, **overrides) -> FileDto:
        defaults = {
            "id": fake_data_factory.ID(),
            "name": fake_data_factory.title(),
            "size": fake_data_factory.integer(),
            "url": fake_data_factory.url(),
        }
        defaults.update(overrides)
        return FileDto(**defaults) if not to_dict else defaults

    @classmethod
    def create_dto(cls, to_dict: bool = False, **overrides) -> CreateFileDto:
        defaults = {
            "name": fake_data_factory.title(),
            "size": fake_data_factory.integer(),
            "url": fake_data_factory.url(),
        }
        defaults.update(overrides)
        return CreateFileDto(**defaults) if not to_dict else defaults

    @classmethod
    def update_dto(cls, to_dict: bool = False, **overrides) -> UpdateFileDto:
        defaults = {
            "name": fake_data_factory.title(),
            "size": fake_data_factory.integer(),
            "url": fake_data_factory.url(),
        }
        defaults.update(overrides)
        return UpdateFileDto(**defaults) if not to_dict else defaults
