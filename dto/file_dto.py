from typing import TypeVar
from pydantic import BaseModel
from fastapi import UploadFile


class FileDto(BaseModel):
    id: int
    name: str
    size: int
    url: str
    article_id: int


class CreateFileDto(BaseModel):
    file: UploadFile
    article_id: int


class UpdateFileDto(CreateFileDto):
    pass


DTOType = TypeVar("DTOType", bound=FileDto)
