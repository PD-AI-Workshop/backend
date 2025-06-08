from fastapi import APIRouter, Depends
from dto.article_dto import ArticleDto, CreateArticleDto, UpdateArticleDto
from service.article_service import ArticleService
from dependencies.article_dependencies import get_article_service


article_controller = APIRouter()


@article_controller.get("/")
async def get_all(service: ArticleService = Depends(get_article_service)) -> list[ArticleDto]:
    return await service.get_all()


@article_controller.get("/{id}")
async def get_by_id(id: int, service: ArticleService = Depends(get_article_service)) -> ArticleDto:
    return await service.get_by_id(id)


@article_controller.post("/")
async def create(dto: CreateArticleDto, service: ArticleService = Depends(get_article_service)) -> ArticleDto:
    return await service.create(dto)


@article_controller.put("/{id}")
async def update(id: int, dto: UpdateArticleDto, service: ArticleService = Depends(get_article_service)) -> None:
    await service.update(id=id, dto=dto)


@article_controller.delete("/{id}")
async def delete(id: int, service: ArticleService = Depends(get_article_service)) -> None:
    await service.delete(id)
