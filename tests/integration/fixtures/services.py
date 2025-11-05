import pytest_asyncio
from redis import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from repository.category_repository import CategoryRepository
from service.category_service import CategoryService
from mapper.category_mapper import CategoryMapper

from repository.article_repository import ArticleRepository
from service.article_service import ArticleService
from mapper.article_mapper import ArticleMapper

from repository.user_repository import UserRepository

from repository.file_repository import FileRepository
from service.file_service import FileService
from mapper.file_mapper import FileMapper


@pytest_asyncio.fixture(scope="function")
async def category_service(session_maker: async_sessionmaker):
    async with session_maker() as session:
        repo = CategoryRepository(session)
        yield CategoryService(repo, CategoryMapper)


@pytest_asyncio.fixture(scope="function")
async def article_service(session_maker: async_sessionmaker, redis_client: Redis):
    async with session_maker() as session:
        article_repo = ArticleRepository(session)
        user_repo = UserRepository(session)

        yield ArticleService(
            repository=article_repo,
            user_repository=user_repo,
            mapper=ArticleMapper,
            redis_client=redis_client,
        )


@pytest_asyncio.fixture(scope="function")
async def file_service(session_maker: async_sessionmaker):
    async with session_maker() as session:
        file_repo = FileRepository(session)
        article_repo = ArticleRepository(session)

        yield FileService(
            repository=file_repo,
            article_repository=article_repo,
            mapper=FileMapper,
        )
