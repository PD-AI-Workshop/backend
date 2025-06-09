from fastapi import Depends
from mapper.file_mapper import FileMapper
from service.file_service import FileService
from repository.file_repository import FileRepository


def get_file_repository() -> FileRepository:
    return FileRepository()


def get_file_mapper() -> FileMapper:
    return FileMapper()


def get_file_service(
    repository: FileRepository = Depends(get_file_repository), mapper: FileMapper = Depends(get_file_mapper)
) -> FileService:
    return FileService(repository=repository, mapper=mapper)
