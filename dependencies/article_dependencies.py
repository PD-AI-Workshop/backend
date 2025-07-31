from fastapi import Depends
from redis import Redis
from mapper.article_mapper import ArticleMapper
from repository.user_repository import UserRepository
from service.article_service import ArticleService
from repository.article_repository import ArticleRepository
from settings import settings


def get_article_repository() -> ArticleRepository:
    return ArticleRepository()


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_article_mapper() -> ArticleMapper:
    return ArticleMapper()


def get_redis_client() -> Redis:
    return settings.redis_client


def get_article_service(
    repository: ArticleRepository = Depends(get_article_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    mapper: ArticleMapper = Depends(get_article_mapper),
    redis_client: Redis = Depends(get_redis_client),
) -> ArticleService:
    return ArticleService(
        repository=repository, mapper=mapper, redis_client=redis_client, user_repository=user_repository
    )
