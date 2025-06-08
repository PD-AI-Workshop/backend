from fastapi import APIRouter, Depends
from service.category_service import CategoryService
from dependencies.category_dependencies import get_category_service
from dto.category_dto import CategoryDto, CreateCategoryDto, UpdateCategoryDto

category_controller = APIRouter()


@category_controller.get("/")
async def get_all(service: CategoryService = Depends(get_category_service)) -> list[CategoryDto]:
    return await service.get_all()


@category_controller.get("/{id}")
async def get_by_id(id: int, service: CategoryService = Depends(get_category_service)) -> CategoryDto:
    return await service.get_by_id(id)


@category_controller.post("/")
async def create(dto: CreateCategoryDto, service: CategoryService = Depends(get_category_service)) -> CategoryDto:
    return await service.create(dto)


@category_controller.put("/{id}")
async def update(id: int, dto: UpdateCategoryDto, service: CategoryService = Depends(get_category_service)) -> None:
    await service.update(id, dto)


@category_controller.delete("/{id}")
async def delete(id: int, service: CategoryService = Depends(get_category_service)) -> None:
    await service.delete(id)
