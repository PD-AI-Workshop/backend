from model.base import ModelType
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from repository.abstract_repository import AbstractRepository


class CRUDBaseRepository(AbstractRepository):
    model: ModelType = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> ModelType:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def create(self, data) -> ModelType:
        query = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        await self.session.commit()

        return result.scalar_one_or_none()

    async def update(self, id: int, data) -> None:
        query = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
        await self.session.execute(query)
        await self.session.commit()

    async def delete(self, id: int) -> None:
        query = delete(self.model).where(self.model.id == id)
        await self.session.execute(query)
        await self.session.commit()
