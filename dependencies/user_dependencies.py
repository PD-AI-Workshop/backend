from repository.user_repository import UserRepository
from db.session import db_session


async def get_user_repository() -> UserRepository:
    async for session in db_session():
        return UserRepository(session)
