import pytest
from http import HTTPStatus

from tests.api.utils.allure.setup import (
    allure_class_setup,
    allure_test_setup,
    Severity,
    Epic,
    Feature,
    Tag,
    Story,
)
from tests.core.schemas.resources.auth_schema import RegisterUserRequestSchema, LoginUserRequestSchema
from tests.core.clients.resources.auth_client import AuthClient
from tests.core.clients.resources.user_client import UserClient

from tests.api.utils.assertions.base import assert_status_code, assert_is_true


@pytest.mark.asyncio
@pytest.mark.api
@pytest.mark.auth
@allure_class_setup(
    severity=Severity.BLOCKER,
    tags=[Tag.SMOKE, Tag.REGRESS],
    epic=Epic.USER_SERVICE,
    feature=Feature.AUTH,
)
class TestAuthPositive:
    @allure_test_setup(title="Successfull registration", story=Story.CREATE)
    async def test_registration_success(
        self,
        auth_client_public: AuthClient,
        user_client_public: UserClient,
        user_data_to_register: RegisterUserRequestSchema,
    ):
        register_response = await auth_client_public.register(user_data_to_register)
        login_data = LoginUserRequestSchema(
            username=user_data_to_register.email, password=user_data_to_register.password
        )
        login_response = await auth_client_public.login(login_data)

        assert_is_true(auth_client_public.session)

        user_client_public.make_private(auth_client_public.session)
        get_auth_user_response = await user_client_public.get_me()

        assert_status_code(register_response.status_code, HTTPStatus.CREATED)
        assert_status_code(login_response.status_code, HTTPStatus.OK)
        assert_status_code(get_auth_user_response.status_code, HTTPStatus.OK)
