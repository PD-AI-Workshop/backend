import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from repository.file_repository import FileRepository
from tests.core.data.dto.file_factory import FileDTOFactory
from model.file import File


@pytest.mark.integration
class TestFileRepositoryDatabaseIntegration:
    TARGET_ID = 1

    @pytest.mark.asyncio
    async def test_get_all(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = FileRepository(session)
            result = await repo.get_all()

            assert all(isinstance(item, File) for item in result)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_by_id(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = FileRepository(session)
            result = await repo.get_by_id(id=self.TARGET_ID)

            assert isinstance(result, File)
            assert result.id == self.TARGET_ID

    @pytest.mark.asyncio
    async def test_create(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = FileRepository(session)
            data = FileDTOFactory.create_dto(to_dict=True)
            result = await repo.create(data)

            assert isinstance(result, File)
            assert result.name == data["name"]

    @pytest.mark.asyncio
    async def test_update(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = FileRepository(session)
            data = FileDTOFactory.update_dto(to_dict=True)
            await repo.update(self.TARGET_ID, data)
            result = await repo.get_by_id(id=self.TARGET_ID)

            assert result.name == data["name"]

    @pytest.mark.asyncio
    async def test_delete(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = FileRepository(session)
            await repo.delete(id=self.TARGET_ID)
            result = await repo.get_by_id(id=self.TARGET_ID)

            assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, session_maker: async_sessionmaker):
        async with session_maker() as session:
            repo = FileRepository(session)
            result = await repo.get_by_id(id=99999)
            assert result is None
