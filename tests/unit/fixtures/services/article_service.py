import pytest
from redis import Redis
from unittest.mock import create_autospec

from service.article_service import ArticleService
from repository.article_repository import ArticleRepository
from repository.user_repository import UserRepository
from mapper.article_mapper import ArticleMapper
from dto.article_dto import ArticleDto
from model.article import Article


@pytest.fixture(scope="function")
def user_mock_repository() -> UserRepository:
    return create_autospec(UserRepository)


@pytest.fixture(scope="function")
def article_mock_mapper() -> ArticleMapper:
    return create_autospec(ArticleMapper)


@pytest.fixture(scope="function")
def article_mock_repository() -> ArticleRepository:
    return create_autospec(ArticleRepository)


@pytest.fixture(scope="function")
def article_service(
    article_mock_mapper: ArticleMapper,
    article_mock_repository: ArticleRepository,
    mock_redis_client: Redis,
    user_mock_repository: UserRepository,
) -> ArticleService:
    return ArticleService(
        repository=article_mock_repository,
        mapper=article_mock_mapper,
        redis_client=mock_redis_client,
        user_repository=user_mock_repository,
    )


@pytest.fixture(scope="session")
def sample_article_orm(sample_article_dto: ArticleDto) -> dict:
    return sample_article_dto.model_dump()


@pytest.fixture(scope="session")
def article(sample_article_dto: ArticleDto) -> Article:
    return Article(
        title=sample_article_dto.title,
        created_date=sample_article_dto.created_date,
        time_reading=sample_article_dto.time_reading,
        main_image_url=sample_article_dto.main_image_url,
        text_id=sample_article_dto.text_id,
        user_id=sample_article_dto.user_id,
    )
