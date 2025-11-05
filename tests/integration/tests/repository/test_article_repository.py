import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from repository.article_repository import ArticleRepository
from tests.core.data.dto.article_factory import ArticleDTOFactory
from model.article import Article
from db.session import async_session_maker


@pytest.mark.integration
class TestArticleRepositoryDatabaseIntegration:
    TARGET_ID = 1

    @pytest.mark.asyncio
    async def test_get_all(self):
        async with async_session_maker() as session:
            repo = ArticleRepository(session)
            result = await repo.get_all()

            assert all(isinstance(item, Article) for item in result)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_by_id(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = ArticleRepository(session)
            result = await repo.get_by_id(id=self.TARGET_ID)

            assert isinstance(result, Article)
            assert result.id == self.TARGET_ID

    @pytest.mark.asyncio
    async def test_create(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = ArticleRepository(session)
            overrides = {"category_ids": [1, 2], "image_ids": [3]}
            data = ArticleDTOFactory.create_dto(to_dict=True, **overrides)
            data.update({"user_id": 2})

            result = await repo.create(data)

            assert isinstance(result, Article)
            assert result.title == data["title"]

    @pytest.mark.asyncio
    async def test_update(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = ArticleRepository(session)
            overrides = {"category_ids": [1, 2], "image_ids": [3]}
            data = ArticleDTOFactory.update_dto(to_dict=True, **overrides)

            await repo.update(self.TARGET_ID, data)
            result = await repo.get_by_id(id=self.TARGET_ID)

            assert result.title == data["title"]

    @pytest.mark.asyncio
    async def test_delete(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = ArticleRepository(session)
            await repo.delete(id=self.TARGET_ID)
            result = await repo.get_by_id(id=self.TARGET_ID)

            assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, session_maker):
        async with session_maker() as session:
            repo = ArticleRepository(session)
            result = await repo.get_by_id(id=99999)
            assert result is None
