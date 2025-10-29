from dto.article_dto import ArticleDto, CreateArticleDto, UpdateArticleDto
from tests.core.data.fake_data_factory import fake_data_factory
from tests.core.data.dto.base_factory import BaseDTOFactory


class ArticleDTOFactory(BaseDTOFactory[ArticleDto]):
    @classmethod
    def dto(cls, **overrides) -> ArticleDto:
        defaults = {
            "id": fake_data_factory.ID(),
            "title": fake_data_factory.title(),
            "created_date": fake_data_factory.datetime(),
            "time_reading": fake_data_factory.time_reading(),
            "main_image_url": fake_data_factory.url(),
            "text_id": fake_data_factory.ID(),
            "user_id": fake_data_factory.ID(),
            "username": fake_data_factory.username(),
            "category_ids": fake_data_factory.list_with_ids(),
            "image_ids": fake_data_factory.list_with_ids(),
        }
        defaults.update(overrides)
        return ArticleDto(**defaults)

    @classmethod
    def create_dto(cls, **overrides) -> CreateArticleDto:
        defaults = {
            "title": fake_data_factory.title(),
            "time_reading": fake_data_factory.time_reading(),
            "main_image_url": fake_data_factory.url(),
            "text_id": fake_data_factory.ID(),
            "category_ids": fake_data_factory.list_with_ids(),
            "image_ids": fake_data_factory.list_with_ids(),
        }
        defaults.update(overrides)
        return CreateArticleDto(**defaults)

    @classmethod
    def update_dto(cls, **overrides) -> UpdateArticleDto:
        defaults = {
            "title": fake_data_factory.title(),
            "time_reading": fake_data_factory.time_reading(),
            "main_image_url": fake_data_factory.url(),
            "text_id": fake_data_factory.ID(),
            "category_ids": fake_data_factory.list_with_ids(),
            "image_ids": fake_data_factory.list_with_ids(),
        }
        defaults.update(overrides)
        return UpdateArticleDto(**defaults)
