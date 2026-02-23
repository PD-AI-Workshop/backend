import pytest
from typing import List

from tests.core.schemas.resources.category_schema import CategorySchema
from tests.core.schemas.resources.file_schema import FileSchema
from tests.core.schemas.resources.article_schema import ArticleSchema
from tests.core.clients.resources.article_client import ArticleClient
from tests.core.clients.resources.category_client import CategoryClient
from tests.core.clients.resources.file_client import FileClient
from tests.api.utils.assertions.category import assert_get_all_response as assert_get_all_categories_response
from tests.api.utils.assertions.article import assert_get_all_response as assert_get_all_articles_response
from tests.api.utils.assertions.file import assert_get_all_response as assert_get_all_files_response
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
    severity=Severity.CRITICAL,
    tags=[Tag.SMOKE, Tag.E2E],
    epic=Epic.E2E_ARTICLE_SERVICE,
    feature=Feature.ARTICLE
)
class TestSuccessGetArticlesScenario:
    @allure_test_setup(title="Successfull getting articles scenario", story=Story.GET)
    async def test_scenario(
        self,
        category_client_private: CategoryClient,
        article_client_private: ArticleClient,
        file_client_private: FileClient,
        multiple_test_articles: List[ArticleSchema],
        multiple_test_categories: List[CategorySchema],
        multiple_test_files: List[FileSchema],
    ):
        get_all_categories_response = await category_client_private.get_all()
        assert_get_all_categories_response(get_all_categories_response, multiple_test_categories)

        get_all_articles_response = await article_client_private.get_all()
        assert_get_all_articles_response(get_all_articles_response, multiple_test_articles)

        get_all_files_response = await file_client_private.get_all()
        assert_get_all_files_response(get_all_files_response, multiple_test_files)



