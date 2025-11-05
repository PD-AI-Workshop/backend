import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from repository.user_repository import UserRepository
from model.user import User


@pytest.mark.integration
class TestUserRepositoryDatabaseIntegration:
    TARGET_ID = 1

    @pytest.mark.asyncio
    async def test_get_all_users(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = UserRepository(session)
            result = await repo.get_all_users()

            assert all(isinstance(item, User) for item in result)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = UserRepository(session)
            result = await repo.get_user_by_id(id=self.TARGET_ID)

            assert isinstance(result, User)
            assert result.id == self.TARGET_ID

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = UserRepository(session)
            result = await repo.get_user_by_id(id=99999)
            assert result is None
