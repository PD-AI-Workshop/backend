import pytest

from tests.core.schemas.resources.category_schema import CreateCategoryRequestSchema, CategorySchema
from tests.core.schemas.resources.article_schema import CreateArticleRequestSchema
from tests.core.schemas.resources.file_schema import FileSchema
from tests.core.clients.resources.article_client import ArticleClient
from tests.core.clients.resources.category_client import CategoryClient
from tests.api.utils.assertions.category import assert_create_response as assert_create_category_response
from tests.api.utils.assertions.article import assert_create_response as assert_create_article_response
from tests.api.utils.assertions.article import assert_delete_by_id_response as assert_delete_article_by_id_response
from tests.api.utils.assertions.article import assert_get_by_id_not_found_response
from tests.api.utils.assertions.category import assert_get_all_response
from tests.api.utils.allure.setup import (
    allure_class_setup,
    allure_test_setup,
    Severity,
    Epic,
    Feature,
    Tag,
    Story,
)


@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.article
@pytest.mark.e2e
@allure_class_setup(
    severity=Severity.CRITICAL, tags=[Tag.SMOKE, Tag.E2E], epic=Epic.E2E_ARTICLE_SERVICE, feature=Feature.ARTICLE
)
class TestSuccessCreateDeleteArticleScenario:
    @allure_test_setup(title="Successfull creating-deleting article scenario", story=Story.CREATE)
    async def test_scenario(
        self,
        category_client_private_admin: CategoryClient,
        article_client_private_admin: ArticleClient,
        category_data_to_create: CreateCategoryRequestSchema,
        test_file: FileSchema,
    ):
        create_category_response = await category_client_private_admin.create(category_data_to_create)
        assert_create_category_response(create_category_response, category_data_to_create)

        get_all_categories_response = await category_client_private_admin.get_all()
        assert_get_all_response(
            get_all_categories_response, [CategorySchema(**create_category_response.data.model_dump())]
        )

        article_data_to_create = CreateArticleRequestSchema(
            main_image_url=test_file.url, image_ids=[test_file.id], category_ids=[create_category_response.data.id]
        )
        create_article_response = await article_client_private_admin.create(article_data_to_create)
        assert_create_article_response(create_article_response, article_data_to_create)

        delete_article_response = await article_client_private_admin.delete(create_article_response.data.id)
        assert_delete_article_by_id_response(delete_article_response)

        get_article_by_id_response = await article_client_private_admin.get(create_article_response.data.id)
        assert_get_by_id_not_found_response(get_article_by_id_response)
