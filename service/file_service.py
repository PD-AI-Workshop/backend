from fastapi import HTTPException, UploadFile
from settings import settings as minio
from mapper.file_mapper import FileMapper
from repository.file_repository import FileRepository
from repository.article_repository import ArticleRepository
from dto.file_dto import FileDto
from exception.file_not_found_exception import FileNotFoundException
from pathlib import Path
from fastapi.responses import StreamingResponse
from minio.error import S3Error

import uuid


class FileService:
    def __init__(self, repository: FileRepository, mapper: FileMapper, article_repository: ArticleRepository):
        self.mapper = mapper
        self.repository = repository
        self.article_repository = article_repository

    async def get_all(self) -> list[FileDto]:
        files = await self.repository.get_all()
        return [self.mapper.to_dto(dto_model=FileDto, orm_model=file) for file in files]

    async def get_by_id(self, id: int) -> FileDto:
        file = await self.repository.get_by_id(id)

        if not (file):
            raise FileNotFoundException()

        return self.mapper.to_dto(dto_model=FileDto, orm_model=file)

    async def get_file(self, filename: str) -> StreamingResponse:
        try:
            response = minio.client.get_object("files", filename)

            return StreamingResponse(
                response.stream(32 * 1024),
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"inline; filename={filename}"},
            )

        except S3Error:
            raise HTTPException(status_code=404, detail="File not found")

    async def create(self, file: UploadFile) -> FileDto:
        file_extension = Path(file.filename).suffix
        stored_filename = f"{uuid.uuid4()}{file_extension}"

        await minio.upload_file(file, object_name=stored_filename)

        file_dict = {
            "name": file.filename,
            "size": file.size,
            "url": f"http://{minio.HOST}/api/files/content/{stored_filename}",
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
            "size": file.size,
            "url": f"{minio.HOST}/api/files/content/{new_filename}",
        }

        await self.repository.update(id, file_dict)

    async def delete(self, id: int) -> None:
        file = await self.repository.get_by_id(id)

        if not (file):
            raise FileNotFoundException()

        filename_in_storage = Path(file.url).name

        await minio.delete_file(filename_in_storage)
        await self.repository.delete(id)

    async def delete_all_unused(self) -> None:
        articles = await self.article_repository.get_all()
        files = await self.repository.get_all()
        used_main_urls = {article.main_image_url for article in articles}
        used_image_ids = set()
        used_text_ids = {article.text_id for article in articles}

        for article in articles:
            used_image_ids.update(article.image_ids)

        unused_files = [
            file
            for file in files
            if (file.url not in used_main_urls and file.id not in used_image_ids and file.id not in used_text_ids)
        ]

        for unused_file in unused_files:
            await self.repository.delete(unused_file.id)
