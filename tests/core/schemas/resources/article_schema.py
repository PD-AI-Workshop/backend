from pydantic import Field
from datetime import datetime
from typing import List, Optional

from tests.core.data.fake_data_factory import fake_data_factory
from tests.core.schemas.base import BaseSchema


class ArticleSchema(BaseSchema):
    id: int
    title: str
    created_date: datetime
    time_reading: int
    main_image_url: str
    text_id: int
    user_id: int
    username: Optional[str]
    category_ids: List[int]
    image_ids: List[int]


class CreateArticleRequestSchema(BaseSchema):
    title: str = Field(default_factory=fake_data_factory.title)
    time_reading: int = Field(default_factory=fake_data_factory.time_reading)
    main_image_url: str
    text_id: int = Field(default_factory=fake_data_factory.integer)
    category_ids: List[int]
    image_ids: List[int]


class CreateArticleResponseSchema(ArticleSchema):
    pass


class GetArticleResponseSchema(ArticleSchema):
    pass


class UpdateArticleRequestSchema(CreateArticleRequestSchema):
    pass
