from dto.category_dto import CategoryDto, CreateCategoryDto, UpdateCategoryDto
from tests.core.data.dto.base_factory import BaseDTOFactory
from tests.core.data.fake_data_factory import fake_data_factory


class CategoryDTOFactory(BaseDTOFactory[CategoryDto]):
    @classmethod
    def dto(cls, **overrides) -> CategoryDto:
        defaults = {
            "id": fake_data_factory.ID(),
            "name": fake_data_factory.title(),
        }
        defaults.update(overrides)
        return CategoryDto(**defaults)

    @classmethod
    def create_dto(cls) -> CreateCategoryDto:
        defaults = {"name": fake_data_factory.title()}
        return CreateCategoryDto(**defaults)

    @classmethod
    def update_dto(cls) -> UpdateCategoryDto:
        defaults = {"name": fake_data_factory.title()}
        return UpdateCategoryDto(**defaults)
