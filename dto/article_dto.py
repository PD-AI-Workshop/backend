from datetime import datetime
from typing import TypeVar
from pydantic import BaseModel


class ArticleDto(BaseModel):
    id: int
    title: str
    created_date: datetime
    time_reading: int
    main_image_url: str
    text_id: int
    user_id: int


class CreateArticleDto(BaseModel):
    title: str
    time_reading: int
    main_image_url: str
    text_id: int
    user_id: int


class UpdateArticleDto(CreateArticleDto):
    pass


DTOType = TypeVar("DTOType", bound=ArticleDto)
