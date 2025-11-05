import pytest
import json
from redis import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from service.article_service import ArticleService
from repository.user_repository import UserRepository
from dto.article_dto import ArticleDto
from tests.core.data.dto.article_factory import ArticleDTOFactory
from exception.article_not_found_exception import ArticleNotFoundException


@pytest.mark.integration
class TestArticleServiceIntegration:
    TARGET_ID = 1

    @pytest.mark.asyncio
    async def test_get_all(self, article_service: ArticleService, redis_client: Redis):
        result = await article_service.get_all()
        redis_data_json = redis_client.get("articles:all")
        redis_article_data = json.loads(redis_data_json)

        assert len(redis_article_data) > 0 and len(result) > 0
        assert len(result) == len(redis_article_data)
        assert all(isinstance(item, ArticleDto) for item in result)

    @pytest.mark.asyncio
    async def test_get_by_id(self, article_service: ArticleService, redis_client: Redis):
        result = await article_service.get_by_id(id=self.TARGET_ID)
        redis_data_json = redis_client.get(f"article:{self.TARGET_ID}")
        redis_article_data = json.loads(redis_data_json)

        assert redis_article_data["id"] == self.TARGET_ID
        assert result.id == self.TARGET_ID
        assert isinstance(result, ArticleDto)

    @pytest.mark.asyncio
    async def test_create(
        self, article_service: ArticleService, session_maker: async_sessionmaker, redis_client: Redis
    ):
        overrides = {"category_ids": [1, 2], "image_ids": [3]}
        data = ArticleDTOFactory.create_dto(**overrides)

        async with session_maker() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_user_by_id(id=1)

        result = await article_service.create(dto=data, user=user)
        redis_data = redis_client.get("articles:all")

        assert redis_data is None
        assert isinstance(result, ArticleDto)

    @pytest.mark.asyncio
    async def test_update(
        self, article_service: ArticleService, session_maker: async_sessionmaker, redis_client: Redis
    ):
        overrides = {"category_ids": [1, 2], "image_ids": [3]}
        data = ArticleDTOFactory.update_dto(**overrides)

        async with session_maker() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_user_by_id(id=1)

        await article_service.update(id=self.TARGET_ID, dto=data, user=user)
        articles_redis_data = redis_client.get("articles:all")
        article_redis_data = redis_client.get(f"article:{self.TARGET_ID}")

        result = await article_service.get_by_id(id=self.TARGET_ID)

        assert result.title == data.title
        assert articles_redis_data is None
        assert article_redis_data is None

    @pytest.mark.asyncio
    async def test_delete(self, article_service: ArticleService, redis_client: Redis):
        await article_service.delete(id=self.TARGET_ID)
        with pytest.raises(ArticleNotFoundException):
            await article_service.get_by_id(id=self.TARGET_ID)

        articles_redis_data = redis_client.get("articles:all")
        article_redis_data = redis_client.get(f"article:{self.TARGET_ID}")

        assert articles_redis_data is None
        assert article_redis_data is None
