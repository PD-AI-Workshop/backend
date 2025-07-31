from sqlalchemy import select
from model.user import User
from db.session import async_session_maker


class UserRepository:
    async def get_all_users(self) -> list[User]:
        async with async_session_maker() as session:
            query = select(User)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_user_by_id(self, id: int) -> User:
        async with async_session_maker() as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()


repository = UserRepository()
