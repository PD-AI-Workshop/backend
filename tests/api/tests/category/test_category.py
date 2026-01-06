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

from tests.core.clients.resources.category_client import CategoryClient
from tests.core.schemas.resources.category_schema import (
    CategorySchema,
    CreateCategoryRequestSchema,
    UpdateCategoryRequestSchema,
)

from tests.api.utils.assertions.category import (
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
    severity=Severity.CRITICAL,
    tags=[Tag.SMOKE, Tag.REGRESS],
    epic=Epic.ARTICLE_SERVICE,
    feature=Feature.CATEGORY,
)
class TestCategoryPositive:
    @allure_test_setup(title="Get all categories", story=Story.GET)
    async def test_get_all(
        self, category_client_private_admin: CategoryClient, multiple_test_categories: List[CategorySchema]
    ):
        get_all_categories_response = await category_client_private_admin.get_all()

        assert_get_all_response(get_all_categories_response, multiple_test_categories)

    @allure_test_setup(title="Get category by id", story=Story.GET)
    async def test_get_by_id(self, category_client_private_admin: CategoryClient, test_category: CategorySchema):
        get_category_response = await category_client_private_admin.get(id=test_category.id)

        assert_get_by_id_response(get_category_response, test_category)

    @allure_test_setup(title="Create category", story=Story.CREATE)
    async def test_create(
        self, category_client_private_admin: CategoryClient, category_data_to_create: CreateCategoryRequestSchema
    ):
        create_category_response = await category_client_private_admin.create(category_data_to_create)

        assert_create_response(create_category_response, category_data_to_create)

    @allure_test_setup(title="Get category by id", story=Story.UPDATE)
    async def test_update_by_id(
        self,
        category_client_private_admin: CategoryClient,
        test_category: CategorySchema,
        category_data_to_update: UpdateCategoryRequestSchema,
    ):
        update_category_response = await category_client_private_admin.update(
            id=test_category.id, data=category_data_to_update
        )

        assert_update_by_id_response(update_category_response)

    @allure_test_setup(title="Delete category by id", story=Story.DELETE)
    async def test_delete_by_id(self, category_client_private_admin: CategoryClient, test_category: CategorySchema):
        delete_category_response = await category_client_private_admin.delete(id=test_category.id)

        assert_delete_by_id_response(delete_category_response)
