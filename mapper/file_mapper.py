from dto.file_dto import DTOType
from model.base import ModelType


class FileMapper:
    @classmethod
    def to_dto(cls, orm_model: ModelType, dto_model: DTOType) -> DTOType:
        return dto_model.model_validate(orm_model, from_attributes=True)

    @classmethod
    def to_dict(cls, dto_model: DTOType) -> dict:
        return dto_model.model_dump(exclude_none=True)

    @classmethod
    def to_model(cls, orm_class: ModelType, dto_model: DTOType) -> ModelType:
        return orm_class(**dto_model.model_dump())
