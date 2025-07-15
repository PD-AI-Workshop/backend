from typing import TypeVar
from pydantic import BaseModel


class FileDto(BaseModel):
    id: int
    name: str
    size: int
    url: str
    article_id: int


DTOType = TypeVar("DTOType", bound=FileDto)
