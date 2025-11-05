from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from settings import settings

async_engine = create_async_engine(settings.POSTGRES_URL)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
