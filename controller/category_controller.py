from fastapi import APIRouter, Depends
from service.category_service import CategoryService
from dependencies.category_dependencies import get_category_service
from dto.category_dto import CategoryDto, CreateCategoryDto, UpdateCategoryDto
from dependencies.role_dependencies import admin_dependency

category_controller = APIRouter()


@category_controller.get("/")
async def get_all(service: CategoryService = Depends(get_category_service)) -> list[CategoryDto]:
    return await service.get_all()


@category_controller.get("/{id}")
async def get_by_id(id: int, service: CategoryService = Depends(get_category_service)) -> CategoryDto:
    return await service.get_by_id(id)


@category_controller.post("/", dependencies=admin_dependency)
async def create(dto: CreateCategoryDto, service: CategoryService = Depends(get_category_service)) -> CategoryDto:
    return await service.create(dto)


@category_controller.put("/{id}", dependencies=admin_dependency)
async def update(id: int, dto: UpdateCategoryDto, service: CategoryService = Depends(get_category_service)) -> None:
    await service.update(id, dto)


@category_controller.delete("/{id}", dependencies=admin_dependency)
async def delete(id: int, service: CategoryService = Depends(get_category_service)) -> None:
    await service.delete(id)
