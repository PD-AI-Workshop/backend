import pytest

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
from tests.core.schemas.resources.user_schema import UserWithPasswordSchema
from tests.core.clients.resources.auth_client import AuthClient
from tests.api.utils.assertions.auth import (
    assert_register_response,
    assert_login_response,
    assert_logout_response,
    assert_register_user_already_exists_response,
    assert_register_user_short_password_response,
    assert_login_invalid_credentials_response,
)
from tests.core.data.fake_data_factory import fake_data_factory


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
        user_data_to_register: RegisterUserRequestSchema,
    ):
        register_response = await auth_client_public.register(user_data_to_register)

        assert_register_response(response=register_response, request=user_data_to_register)

    @allure_test_setup(title="Successfull login", story=Story.LOGIN)
    async def test_login_success(
        self,
        auth_client_public: AuthClient,
        test_user: UserWithPasswordSchema,
    ):
        data_to_login = LoginUserRequestSchema(username=test_user.email, password=test_user.password)
        login_response = await auth_client_public.login(data_to_login)

        assert_login_response(response=login_response)

    @allure_test_setup(title="Successfull logout", story=Story.LOGIN)
    async def test_logout_success(
        self,
        auth_client_private: AuthClient,
    ):
        logout_response = await auth_client_private.logout()

        assert_logout_response(response=logout_response)


@pytest.mark.asyncio
@pytest.mark.api
@pytest.mark.auth
@allure_class_setup(
    severity=Severity.BLOCKER,
    tags=[Tag.REGRESS, Tag.NEGATIVE],
    epic=Epic.USER_SERVICE,
    feature=Feature.AUTH,
)
class TestAuthNegative:
    @allure_test_setup(title="Registration user already exists", story=Story.CREATE)
    async def test_registration_user_already_exists(
        self,
        register_test_user: None,
        auth_client_public: AuthClient,
        user_data_to_register: RegisterUserRequestSchema,
    ):
        register_response = await auth_client_public.register(user_data_to_register)
        assert_register_user_already_exists_response(response=register_response)

    @allure_test_setup(title="Registration user with short password", story=Story.CREATE)
    async def test_registration_user_short_password(
        self,
        register_test_user: None,
        auth_client_public: AuthClient,
        user_data_to_register: RegisterUserRequestSchema,
    ):
        user_data_to_register.password = "*x"
        register_response = await auth_client_public.register(user_data_to_register)
        assert_register_user_short_password_response(response=register_response)

    @allure_test_setup(title="Login with invlid credentials", story=Story.LOGIN)
    async def test_login_invalid_credentials(
        self,
        test_user: UserWithPasswordSchema,
        auth_client_public: AuthClient,
    ):
        data_to_login = LoginUserRequestSchema(username=test_user.email, password=fake_data_factory.title())
        login_response = await auth_client_public.login(data_to_login)

        assert_login_invalid_credentials_response(response=login_response)
