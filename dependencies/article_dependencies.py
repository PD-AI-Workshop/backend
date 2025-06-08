from fastapi import Depends
from mapper.article_mapper import ArticleMapper
from service.article_service import ArticleService
from repository.article_repository import ArticleRepository


def get_article_repository() -> ArticleRepository:
    return ArticleRepository()


def get_article_mapper() -> ArticleMapper:
    return ArticleMapper()


def get_article_service(
    repository: ArticleRepository = Depends(get_article_repository), mapper: ArticleMapper = Depends(get_article_mapper)
) -> ArticleService:
    return ArticleService(repository=repository, mapper=mapper)
