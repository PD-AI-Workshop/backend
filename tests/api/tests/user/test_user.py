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

from tests.core.clients.resources.user_client import UserClient
from tests.core.schemas.resources.user_schema import UserWithPasswordSchema, UpdateUserRequestSchema

from tests.api.utils.assertions.user import (
    assert_get_all_response,
    assert_get_by_id_response,
    assert_update_by_id_response,
    assert_update_current_user_response,
    assert_delete_by_id_response,
)


@pytest.mark.asyncio
@pytest.mark.api
@pytest.mark.user
@allure_class_setup(
    severity=Severity.BLOCKER,
    tags=[Tag.SMOKE, Tag.REGRESS],
    epic=Epic.USER_SERVICE,
    feature=Feature.USER,
)
class TestUserPositive:
    @allure_test_setup(title="Get all users", story=Story.GET)
    async def test_get_all(self, user_client_private_admin: UserClient, multiple_test_users: List[UserWithPasswordSchema]):
        get_all_users_response = await user_client_private_admin.get_all()

        assert_get_all_response(get_all_users_response, multiple_test_users)


    @allure_test_setup(title="Get user by id", story=Story.GET)
    async def test_get_by_id(self, user_client_private_admin: UserClient, test_user: UserWithPasswordSchema):
        get_user_response = await user_client_private_admin.get(id=test_user.id)

        assert_get_by_id_response(get_user_response, test_user)


    @allure_test_setup(title="Get current user", story=Story.GET)
    async def test_get_current_user(self, user_client_private: UserClient, test_user: UserWithPasswordSchema):
        get_current_user_response = await user_client_private.get_me()

        assert_get_by_id_response(get_current_user_response, test_user)


    @allure_test_setup(title="Update user by id", story=Story.UPDATE)
    async def test_update_by_id(
        self, user_client_private_admin: UserClient, test_user: UserWithPasswordSchema, user_data_to_update: UpdateUserRequestSchema
    ):
        update_user_response = await user_client_private_admin.update(id=test_user.id, data=user_data_to_update)
        print(update_user_response)

        assert_update_by_id_response(update_user_response, user_data_to_update)


    @allure_test_setup(title="Update current user", story=Story.UPDATE)
    async def test_update_current_user(
        self, user_client_private: UserClient, user_data_to_update: UpdateUserRequestSchema
    ):
        update_current_user_response = await user_client_private.update_me(data=user_data_to_update)

        assert_update_current_user_response(update_current_user_response, user_data_to_update)


    @allure_test_setup(title="Delete user by id", story=Story.DELETE)
    async def test_delete_by_id(self, user_client_private_admin: UserClient, test_user: UserWithPasswordSchema):
        delete_user_response = await user_client_private_admin.delete(id=test_user.id)

        assert_delete_by_id_response(delete_user_response)
