import pytest_asyncio
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import async_sessionmaker
from pathlib import Path
import os
import uuid
from minio.error import S3Error

from tests.core.utils.logger import logger
from settings import settings
from repository.file_repository import FileRepository


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_bucket(session_maker: async_sessionmaker):
    file_path = "./tests/core/data/static/image.png"
    file_size = os.path.getsize(file_path)

    logger.info("Uploading test data in S3")
    with open(file_path, "rb") as file:
        upload_file = UploadFile(file=file, filename="image.png", size=file_size)

        file_extension = Path(upload_file.filename).suffix
        stored_filename = f"{uuid.uuid4()}{file_extension}"

        await settings.upload_file(upload_file, object_name=stored_filename)

    file_dict = {
        "name": upload_file.filename,
        "size": upload_file.size,
        "url": f"http://{settings.HOST}/api/files/content/{stored_filename}",
    }

    async with session_maker() as session:
        repo = FileRepository(session)
        await repo.create(file_dict)

    yield

    try:
        objects = settings.client.list_objects("files", recursive=True)
        for obj in objects:
            settings.client.remove_object("files", obj.object_name)
        logger.info("Cleaning bucket after test")
    except S3Error as e:
        logger.warning(f"Error cleaning bucket: {e}")
