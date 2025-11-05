from sqlalchemy import select
from model.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from repository.crud_base_repository import CRUDBaseRepository


class CategoryRepository(CRUDBaseRepository):
    model = Category

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all_by_ids(self, ids: list[int]):
        query = select(Category).where(Category.id.in_(ids))
        result = await self.session.execute(query)
        return result.scalars().all()
