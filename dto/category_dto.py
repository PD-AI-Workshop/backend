from typing import TypeVar
from pydantic import BaseModel


class CategoryDto(BaseModel):
    id: int
    name: str


class CreateCategoryDto(BaseModel):
    name: str


class UpdateCategoryDto(CreateCategoryDto):
    pass


DTOType = TypeVar("DTOType", bound=CategoryDto)
