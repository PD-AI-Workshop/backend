from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import dbSettings

async_engine = create_async_engine(dbSettings.POSTGRES_URL)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
