from fastapi import Depends
from mapper.file_mapper import FileMapper
from service.file_service import FileService
from repository.file_repository import FileRepository
from repository.article_repository import ArticleRepository
from dependencies.article_dependencies import get_article_repository
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import db_session


def get_file_repository(session: AsyncSession = Depends(db_session)) -> FileRepository:
    return FileRepository(session)


def get_file_mapper() -> FileMapper:
    return FileMapper()


def get_file_service(
    repository: FileRepository = Depends(get_file_repository),
    mapper: FileMapper = Depends(get_file_mapper),
    article_repository: ArticleRepository = Depends(get_article_repository),
) -> FileService:
    return FileService(repository=repository, mapper=mapper, article_repository=article_repository)
