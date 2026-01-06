from fastapi import Depends
from service.test_service import TestService
from repository.test_repository import TestRepository
from db.session import db_session


async def get_test_repository() -> TestRepository:
    async for session in db_session():
        return TestRepository(session)


def get_test_service(
    repository: db_session = Depends(get_test_repository),
) -> TestService:
    return TestService(repository=repository)
