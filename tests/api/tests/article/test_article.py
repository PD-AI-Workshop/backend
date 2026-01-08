import pytest
from typing import List

from tests.api.utils.allure.setup import (
    allure_class_setup,
    allure_test_setup,
    Severity,
    Epic,
    Feature,
    Tag,
    Story,
)

from tests.core.clients.resources.article_client import ArticleClient
from tests.core.schemas.resources.article_schema import (
    ArticleSchema,
    CreateArticleRequestSchema,
    UpdateArticleRequestSchema,
)

from tests.api.utils.assertions.article import (
    assert_get_all_response,
    assert_delete_by_id_response,
    assert_get_by_id_response,
    assert_update_by_id_response,
    assert_create_response,
)


@pytest.mark.asyncio
@pytest.mark.api
@pytest.mark.category
@allure_class_setup(
    severity=Severity.BLOCKER,
    tags=[Tag.SMOKE, Tag.REGRESS],
    epic=Epic.ARTICLE_SERVICE,
    feature=Feature.ARTICLE,
)
class TestArticlePositive:
    @allure_test_setup(title="Get all articles", story=Story.GET)
    async def test_get_all(self, article_client_public: ArticleClient, multiple_test_articles: List[ArticleSchema]):
        get_all_article_response = await article_client_public.get_all()

        assert_get_all_response(get_all_article_response, multiple_test_articles)

    @allure_test_setup(title="Get article by id", story=Story.GET)
    async def test_get_by_id(self, article_client_private_admin: ArticleClient, test_article: ArticleSchema):
        get_article_response = await article_client_private_admin.get(id=test_article.id)

        assert_get_by_id_response(get_article_response, test_article)

    @allure_test_setup(title="Create article", story=Story.CREATE)
    async def test_create(
        self, article_client_private_admin: ArticleClient, article_data_to_create: CreateArticleRequestSchema
    ):
        create_article_response = await article_client_private_admin.create(article_data_to_create)

        assert_create_response(create_article_response, article_data_to_create)

    @allure_test_setup(title="Get article by id", story=Story.UPDATE)
    async def test_update_by_id(
        self,
        article_client_private_admin: ArticleClient,
        test_article: ArticleSchema,
        article_data_to_update: UpdateArticleRequestSchema,
    ):
        update_article_response = await article_client_private_admin.update(
            id=test_article.id, data=article_data_to_update
        )

        assert_update_by_id_response(update_article_response)

    @allure_test_setup(title="Delete article by id", story=Story.DELETE)
    async def test_delete_by_id(self, article_client_private_admin: ArticleClient, test_article: ArticleSchema):
        delete_article_response = await article_client_private_admin.delete(id=test_article.id)

        assert_delete_by_id_response(delete_article_response)
