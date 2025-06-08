from sqlalchemy import select
from model.category import Category
from db.session import async_session_maker
from repository.crud_base_repository import CRUDBaseRepository


class CategoryRepository(CRUDBaseRepository):
    model = Category

    async def get_all_by_ids(self, ids: list[int]):
        async with async_session_maker() as session:
            query = select(Category).where(Category.id.in_(ids))
            result = await session.execute(query)
            return result.scalars().all()
