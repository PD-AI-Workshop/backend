import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from repository.category_repository import CategoryRepository
from tests.core.data.dto.category_factory import CategoryDTOFactory
from model.category import Category


@pytest.mark.integration
class TestCategoryRepositoryDatabaseIntegration:
    TARGET_ID = 1

    @pytest.mark.asyncio
    async def test_get_all(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = CategoryRepository(session)
            result = await repo.get_all()

            assert all(isinstance(item, Category) for item in result)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_all_by_ids(self, session_maker: async_sessionmaker):
        CATEGORY_IDS = [1, 4]
        async with session_maker() as session:
            repo = CategoryRepository(session)
            result = await repo.get_all_by_ids(ids=CATEGORY_IDS)

            assert all((isinstance(item, Category) and item.id in CATEGORY_IDS) for item in result)
            assert len(result) == len(CATEGORY_IDS)

    @pytest.mark.asyncio
    async def test_get_by_id(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = CategoryRepository(session)
            result = await repo.get_by_id(id=self.TARGET_ID)

            assert isinstance(result, Category)
            assert result.id == self.TARGET_ID

    @pytest.mark.asyncio
    async def test_create(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = CategoryRepository(session)
            data = CategoryDTOFactory.create_dto(to_dict=True)
            created_category = await repo.create(data)

            assert isinstance(created_category, Category)
            assert created_category.name == data["name"]

    @pytest.mark.asyncio
    async def test_update(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = CategoryRepository(session)
            update_data = CategoryDTOFactory.update_dto(to_dict=True)
            await repo.update(id=self.TARGET_ID, data=update_data)
            result = await repo.get_by_id(id=self.TARGET_ID)

            assert result.name == update_data["name"]

    @pytest.mark.asyncio
    async def test_delete(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = CategoryRepository(session)
            await repo.delete(id=self.TARGET_ID)
            result = await repo.get_by_id(id=self.TARGET_ID)

            assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = CategoryRepository(session)
            result = await repo.get_by_id(id=99999)
            assert result is None
