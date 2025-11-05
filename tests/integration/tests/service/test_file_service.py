import pytest
from minio.error import S3Error
import os
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from pathlib import Path

from service.file_service import FileService
from settings import settings as minio
from dto.file_dto import FileDto
from exception.file_not_found_exception import FileNotFoundException


@pytest.mark.integration
class TestFileServiceIntegration:
    # Так как мы заранее заполняем базу тестовыми данными, используем заранее известные IDs
    # Можно изолировать каждый тест, и вынести создание тестовых сущностей в фикстуры (Recommended)
    TARGET_ID = 1
    FILE_ID_UPLOADED_IN_S3 = 4
    UNUSED_FILE_IDS = [3, 4]
    TEST_STATIC_DIR = "./tests/core/data/static"

    @pytest.mark.asyncio
    async def test_get_all(self, file_service: FileService):
        result = await file_service.get_all()

        assert len(result) > 0
        assert all(isinstance(item, FileDto) for item in result)

    @pytest.mark.asyncio
    async def test_get_by_id(self, file_service: FileService):
        result = await file_service.get_by_id(id=self.TARGET_ID)

        assert isinstance(result, FileDto)

    @pytest.mark.asyncio
    async def test_create(self, file_service: FileService):
        file_path = f"{self.TEST_STATIC_DIR}/image.png"
        file_size = os.path.getsize(file_path)

        with open(file_path, "rb") as file:
            upload_file = UploadFile(file=file, filename="image.png", size=file_size)
            result = await file_service.create(file=upload_file)

        file_name = Path(result.url).name
        response = minio.client.get_object("files", file_name)

        assert isinstance(result, FileDto)
        assert response

    @pytest.mark.asyncio
    async def test_get_file(self, file_service: FileService):
        result = await file_service.get_by_id(id=self.FILE_ID_UPLOADED_IN_S3)

        file_name = Path(result.url).name
        result = await file_service.get_file(file_name)

        assert isinstance(result, StreamingResponse)

    @pytest.mark.asyncio
    async def test_update(self, file_service: FileService):
        FILE_TO_UPDATE_NAME = "image2.webp"
        file_path = f"{self.TEST_STATIC_DIR}/{FILE_TO_UPDATE_NAME}"
        file_size = os.path.getsize(file_path)

        previous_file = await file_service.get_by_id(id=self.FILE_ID_UPLOADED_IN_S3)
        previous_file_name = Path(previous_file.url).name

        with open(file_path, "rb") as file:
            upload_file = UploadFile(file=file, filename=FILE_TO_UPDATE_NAME, size=file_size)
            await file_service.update(id=self.FILE_ID_UPLOADED_IN_S3, uploaded_file=upload_file)

        result = await file_service.get_by_id(id=self.FILE_ID_UPLOADED_IN_S3)
        updated_file_name = Path(result.url).name
        updated_file = minio.client.get_object("files", updated_file_name)

        with pytest.raises(S3Error):
            minio.client.get_object("files", previous_file_name)

        assert result.name == FILE_TO_UPDATE_NAME
        assert updated_file

    @pytest.mark.asyncio
    async def test_delete(self, file_service: FileService):
        file_path = f"{self.TEST_STATIC_DIR}/image.png"
        file_size = os.path.getsize(file_path)

        with open(file_path, "rb") as file:
            upload_file = UploadFile(file=file, filename="image.png", size=file_size)
            created_file = await file_service.create(file=upload_file)

        file_name = Path(created_file.url).name
        await file_service.delete(id=created_file.id)

        with pytest.raises(FileNotFoundException):
            await file_service.get_by_id(id=created_file.id)

        with pytest.raises(HTTPException):
            await file_service.get_file(file_name)

    @pytest.mark.asyncio
    async def test_delete_all_unused(self, file_service: FileService):
        await file_service.delete_all_unused()

        for id in self.UNUSED_FILE_IDS:
            with pytest.raises(FileNotFoundException):
                await file_service.get_by_id(id)

    @pytest.mark.asyncio
    async def test_update_not_found(self, file_service: FileService):
        FILE_TO_UPDATE_NAME = "image2.webp"
        file_path = f"{self.TEST_STATIC_DIR}/{FILE_TO_UPDATE_NAME}"
        file_size = os.path.getsize(file_path)

        with open(file_path, "rb") as file:
            upload_file = UploadFile(file=file, filename=FILE_TO_UPDATE_NAME, size=file_size)
            with pytest.raises(FileNotFoundException):
                await file_service.update(id=99999, uploaded_file=upload_file)

    @pytest.mark.asyncio
    async def test_delete_not_found(self, file_service: FileService):
        with pytest.raises(FileNotFoundException):
            await file_service.delete(id=99999)
