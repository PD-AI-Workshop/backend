from mapper.category_mapper import CategoryMapper
from repository.category_repository import CategoryRepository
from exception.category_not_found_exception import CategoryNotFoundException
from dto.category_dto import CategoryDto, CreateCategoryDto, UpdateCategoryDto


class CategoryService:
    def __init__(self, repository: CategoryRepository, mapper: CategoryMapper):
        self.mapper = mapper
        self.repository = repository

    async def get_all(self) -> list[CategoryDto]:
        categories = await self.repository.get_all()
        return [self.mapper.to_dto(orm_model=category, dto_model=CategoryDto) for category in categories]

    async def get_by_id(self, id: int) -> CategoryDto:
        category = await self.repository.get_by_id(id)

        if not (category):
            raise CategoryNotFoundException()

        return self.mapper.to_dto(orm_model=category, dto_model=CategoryDto)

    async def create(self, dto: CreateCategoryDto) -> CategoryDto:
        category_dict = self.mapper.to_dict(dto)
        created_category = await self.repository.create(category_dict)
        return self.mapper.to_dto(orm_model=created_category, dto_model=CategoryDto)

    async def update(self, id: int, dto: UpdateCategoryDto) -> None:
        category_dict = self.mapper.to_dict(dto)
        await self.repository.update(id, category_dict)

    async def delete(self, id: int) -> None:
        await self.repository.delete(id)
