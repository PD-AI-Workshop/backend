from datetime import datetime
from typing import Optional, TypeVar
from pydantic import BaseModel, ConfigDict


class ArticleDto(BaseModel):
    id: int
    title: str
    created_date: datetime
    time_reading: int
    main_image_url: str
    text_id: int
    user_id: int
    username: Optional[str] = None
    category_ids: list[int]
    image_ids: list[int]

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class CreateArticleDto(BaseModel):
    title: str
    time_reading: int
    main_image_url: str
    text_id: int
    category_ids: list[int]
    image_ids: list[int]


class UpdateArticleDto(CreateArticleDto):
    pass


DTOType = TypeVar("DTOType", bound=ArticleDto)
