from fastapi import Depends
from mapper.file_mapper import FileMapper
from service.file_service import FileService
from repository.file_repository import FileRepository
from repository.article_repository import ArticleRepository
from dependencies.article_dependencies import get_article_repository
from db.session import db_session


async def get_file_repository() -> FileRepository:
    async for session in db_session():
        return FileRepository(session)


def get_file_mapper() -> FileMapper:
    return FileMapper()


def get_file_service(
    repository: FileRepository = Depends(get_file_repository),
    mapper: FileMapper = Depends(get_file_mapper),
    article_repository: ArticleRepository = Depends(get_article_repository),
) -> FileService:
    return FileService(repository=repository, mapper=mapper, article_repository=article_repository)
