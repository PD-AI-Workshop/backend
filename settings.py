import io
import json
from minio import Minio
from fastapi import UploadFile
from config.log_config import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    MINIO_HOST: str
    MINIO_PORT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str

    @property
    def client(self):
        return Minio(
            endpoint=f"{self.MINIO_HOST}:{self.MINIO_PORT}",
            access_key=self.MINIO_ACCESS_KEY,
            secret_key=self.MINIO_SECRET_KEY,
            secure=False,
        )

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialize_bucket()

    def _initialize_bucket(self):
        if not self.client.bucket_exists("files"):
            self.client.make_bucket("files")
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": ["arn:aws:s3:::files/*"],
                    }
                ],
            }
            self.client.set_bucket_policy("files", json.dumps(policy))
            logger.info("Bucket created")
        else:
            logger.warning("Bucket already exists")

    async def upload_file(self, file: UploadFile):
        file_data = await file.read()
        file_stream = io.BytesIO(file_data)

        saved_file = self.client.put_object(
            bucket_name="files",
            object_name=file.filename,
            data=file_stream,
            length=len(file_data),
            content_type=file.content_type,
        )

        return saved_file

    async def delete_file(self, file_name: str):
        self.client.remove_object("files", file_name)

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
