from pydantic import Field

from tests.core.data.fake_data_factory import fake_data_factory
from tests.core.schemas.base import BaseSchema


class CategorySchema(BaseSchema):
    id: int
    name: str


class CreateCategoryRequestSchema(BaseSchema):
    name: str = Field(default_factory=fake_data_factory.title)


class CreateCategoryResponseSchema(CategorySchema):
    pass


class GetCategoryResponseSchema(CategorySchema):
    pass


class UpdateCategoryRequestSchema(CreateCategoryRequestSchema):
    pass
