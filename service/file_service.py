from fastapi import UploadFile
from settings import settings as minio
from mapper.file_mapper import FileMapper
from repository.file_repository import FileRepository
from dto.file_dto import FileDto
from exception.file_not_found_exception import FileNotFoundException
from pathlib import Path

import uuid


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

    async def create(self, file: UploadFile) -> FileDto:
        file_extension = Path(file.filename).suffix
        stored_filename = f"{uuid.uuid4()}{file_extension}"

        await minio.upload_file(file, object_name=stored_filename)

        file_dict = {
            "name": file.filename,
            "size": file.size,
            "url": f"http://{minio.MINIO_HOST}:{minio.MINIO_PORT}/files/{stored_filename}",
        }

        created_file = await self.repository.create(file_dict)
        return self.mapper.to_dto(dto_model=FileDto, orm_model=created_file)

    async def update(self, id: int, uploaded_file: UploadFile) -> None:
        file = await self.repository.get_by_id(id)

        if not (file):
            raise FileNotFoundException()

        current_filename = Path(file.url).name
        file_extension = Path(uploaded_file.filename).suffix
        new_filename = f"{uuid.uuid4()}{file_extension}"

        await minio.upload_file(uploaded_file, object_name=new_filename)
        await minio.delete_file(current_filename)

        file_dict = {
            "name": uploaded_file.filename,
            "size": uploaded_file.size,
            "url": f"http://{minio.MINIO_HOST}:{minio.MINIO_PORT}/files/{new_filename}",
        }

        await self.repository.update(id, file_dict)

    async def delete(self, id: int) -> None:
        file = await self.repository.get_by_id(id)

        if not (file):
            raise FileNotFoundException()

        filename_in_storage = Path(file.url).name

        await minio.delete_file(filename_in_storage)
        await self.repository.delete(id)
