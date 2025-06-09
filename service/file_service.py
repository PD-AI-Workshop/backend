from fastapi import UploadFile
from settings import settings as minio
from mapper.file_mapper import FileMapper
from repository.file_repository import FileRepository
from dto.file_dto import CreateFileDto, FileDto, UpdateFileDto
from exception.file_not_found_exception import FileNotFoundException


class FileService:
    def __init__(self, repository: FileRepository, mapper: FileMapper):
        self.mapper = mapper
        self.repository = repository

    async def get_all(self) -> list[FileDto]:
        files = await self.repository.get_all()
        return [self.mapper.to_dto(dto_model=FileDto, orm_model=file) for file in files]

    async def get_by_id(self, id: int) -> FileDto:
        file = await self.repository.get_by_id(id)

        if not (file):
            raise FileNotFoundException()

        return self.mapper.to_dto(dto_model=FileDto, orm_model=file)

    async def create(self, file: UploadFile, article_id: int) -> FileDto:
        await minio.upload_file(file)

        file_dict = {
            "name": file.filename,
            "size": file.size,
            "url": f"http://{minio.MINIO_HOST}:{minio.MINIO_PORT}/files/{file.filename}",
            "article_id": article_id,
        }

        created_file = await self.repository.create(file_dict)
        return self.mapper.to_dto(dto_model=FileDto, orm_model=created_file)

    async def update(self, id: int, uploaded_file: UploadFile, article_id: int) -> None:
        file = await self.repository.get_by_id(id)

        if not (file):
            raise FileNotFoundException()

        await minio.upload_file(uploaded_file)
        await minio.delete_file(file.name)

        file_dict = {
            "name": uploaded_file.filename,
            "size": uploaded_file.size,
            "url": f"http://{minio.MINIO_HOST}:{minio.MINIO_PORT}/files/{uploaded_file.filename}",
            "article_id": article_id,
        }

        await self.repository.update(id, file_dict)

    async def delete(self, id: int) -> None:
        file = await self.repository.get_by_id(id)

        if not (file):
            raise FileNotFoundException()

        await self.repository.delete(id)
        await minio.delete_file(file.name)
