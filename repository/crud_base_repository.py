from model.base import ModelType
from db.session import async_session_maker
from sqlalchemy import delete, insert, select, update
from repository.abstract_repository import AbstractRepository


class CRUDBaseRepository(AbstractRepository):
    model: ModelType = None

    async def get_by_id(cls, id: int) -> ModelType:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def get_all(cls) -> list[ModelType]:
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)

            return result.scalars().all()

    async def create(cls, data) -> ModelType:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()

            return result.scalar_one_or_none()

    async def update(cls, id: int, data) -> None:
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == id).values(**data).returning(cls.model)
            await session.execute(query)
            await session.commit()

    async def delete(cls, id: int) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == id)
            await session.execute(query)
            await session.commit()
