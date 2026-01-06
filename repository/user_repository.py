from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self) -> list[User]:
        query = select(User)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_user_by_id(self, id: int) -> User:
        query = select(User).where(User.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
