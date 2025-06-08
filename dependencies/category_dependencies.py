from fastapi import Depends
from mapper.category_mapper import CategoryMapper
from service.category_service import CategoryService
from repository.category_repository import CategoryRepository


def get_category_repository() -> CategoryRepository:
    return CategoryRepository()


def get_category_mapper() -> CategoryMapper:
    return CategoryMapper()


def get_category_service(
    repository: CategoryRepository = Depends(get_category_repository),
    mapper: CategoryMapper = Depends(get_category_mapper),
) -> CategoryService:
    return CategoryService(repository=repository, mapper=mapper)
