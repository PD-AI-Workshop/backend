from dto.category_dto import CategoryDto, CreateCategoryDto, UpdateCategoryDto
from tests.core.data.dto.base_factory import BaseDTOFactory
from tests.core.data.fake_data_factory import fake_data_factory


class CategoryDTOFactory(BaseDTOFactory[CategoryDto]):
    @classmethod
    def dto(cls, to_dict: bool = False, **overrides) -> CategoryDto:
        defaults = {
            "id": fake_data_factory.ID(),
            "name": fake_data_factory.title(),
        }
        defaults.update(overrides)
        return CategoryDto(**defaults) if not to_dict else defaults

    @classmethod
    def create_dto(cls, to_dict: bool = False) -> CreateCategoryDto:
        defaults = {"name": fake_data_factory.title()}
        return CreateCategoryDto(**defaults) if not to_dict else defaults

    @classmethod
    def update_dto(cls, to_dict: bool = False) -> UpdateCategoryDto:
        defaults = {"name": fake_data_factory.title()}
        return UpdateCategoryDto(**defaults) if not to_dict else defaults
