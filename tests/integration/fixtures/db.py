import pytest_asyncio
import json
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tests.core.utils.logger import logger
from model.base import Base
from model.category import Category
from model.user import User
from model.file import File
from model.article import Article
from settings import settings


def convert_dates(obj, date_keys=("created_date",)):
    for key in date_keys:
        if key in obj and isinstance(obj[key], str):
            obj[key] = datetime.fromisoformat(obj[key])
    return obj


@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(settings.POSTGRES_URL)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session_maker(engine):
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    yield session_maker


@pytest_asyncio.fixture(autouse=True)
async def setup_data(engine, session_maker):
    logger.info("Creating database tables")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        logger.info("Creating test categories")
        with open("./tests/core/data/setup/category.json", "r") as file:
            for obj in json.load(file):
                session.add(Category(**obj))

        logger.info("Creating test users")
        with open("./tests/core/data/setup/user.json", "r") as file:
            for obj in json.load(file):
                session.add(User(**obj))

        logger.info("Creating test files")
        with open("./tests/core/data/setup/file.json", "r") as file:
            for obj in json.load(file):
                session.add(File(**obj))

        await session.commit()

        result = await session.execute(select(Category))
        category_map = {c.id: c for c in result.scalars()}

        result = await session.execute(select(File))
        file_map = {f.id: f for f in result.scalars()}

        result = await session.execute(select(User))
        user_map = {u.id: u for u in result.scalars()}

        logger.info("Creating test articles")
        with open("./tests/core/data/setup/article.json", "r") as file:
            for obj in json.load(file):
                cat_ids = obj.pop("category_ids", [])
                file_ids = obj.pop("image_ids", [])
                obj = convert_dates(obj)

                article = Article(**obj)
                article.categories = [category_map[cid] for cid in cat_ids if cid in category_map]
                article.files = [file_map[fid] for fid in file_ids if fid in file_map]
                article.user = user_map.get(article.user_id)
                session.add(article)

        await session.commit()

    yield

    logger.info("Cleaning database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
