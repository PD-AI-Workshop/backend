import pytest

from tests.core.schemas.resources.auth_schema import LoginUserRequestSchema, RegisterUserRequestSchema
from tests.core.clients.resources.auth_client import AuthClient
from tests.core.clients.resources.user_client import UserClient
from tests.core.schemas.resources.user_schema import UserWithPasswordSchema
from tests.api.utils.assertions.auth import (
    assert_register_response,
    assert_login_response,
    assert_logout_response
)
from tests.api.utils.assertions.user import (
    assert_get_current_user_response
)
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
@pytest.mark.auth
@pytest.mark.e2e
@allure_class_setup(
    severity=Severity.BLOCKER,
    tags=[Tag.SMOKE, Tag.E2E],
    epic=Epic.E2E_USER_SERVICE,
    feature=Feature.AUTH
)
class TestSuccessUserScenario:
    @allure_test_setup(title="Successfull user scenario", story=Story.LOGIN)
    async def test_scenario(
        self,
        auth_client_public: AuthClient,
        user_client_public: UserClient,
        user_data_to_register: RegisterUserRequestSchema,
    ):
        register_response = await auth_client_public.register(user_data_to_register)
        assert_register_response(register_response, user_data_to_register)
        
        login_data = LoginUserRequestSchema(
            username=user_data_to_register.email, password=user_data_to_register.password
        )
        login_response = await auth_client_public.login(login_data)
        assert_login_response(login_response)

        user_client_public.make_private(auth_client_public.session)
        get_current_user_response = await user_client_public.get_me()
        user_with_password_schema = UserWithPasswordSchema(
            id=get_current_user_response.data.id, **user_data_to_register.model_dump()
        )
        assert_get_current_user_response(get_current_user_response, user_with_password_schema)

        logout_response = await auth_client_public.logout()
        assert_logout_response(logout_response)

