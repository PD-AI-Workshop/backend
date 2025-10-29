import pytest

from dto.article_dto import ArticleDto, CreateArticleDto, UpdateArticleDto
from tests.core.data.dto.article_factory import ArticleDTOFactory


@pytest.fixture(scope="session")
def sample_article_dto() -> ArticleDto:
    return ArticleDTOFactory.dto()


@pytest.fixture(scope="session")
def sample_create_article_dto() -> CreateArticleDto:
    return ArticleDTOFactory.create_dto()


@pytest.fixture(scope="session")
def sample_update_dto() -> UpdateArticleDto:
    return ArticleDTOFactory.update_dto()
