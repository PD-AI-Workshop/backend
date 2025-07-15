from fastapi import Depends
from redis import Redis
from mapper.article_mapper import ArticleMapper
from service.article_service import ArticleService
from repository.article_repository import ArticleRepository
from settings import settings


def get_article_repository() -> ArticleRepository:
    return ArticleRepository()


def get_article_mapper() -> ArticleMapper:
    return ArticleMapper()


def get_redis_client() -> Redis:
    return settings.redis_client


def get_article_service(
    repository: ArticleRepository = Depends(get_article_repository), mapper: ArticleMapper = Depends(get_article_mapper), redis_client: Redis = Depends(get_redis_client)
) -> ArticleService:
    return ArticleService(repository=repository, mapper=mapper, redis_client=redis_client)
