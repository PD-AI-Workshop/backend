import pytest
import pytest_asyncio
from httpx import AsyncClient

from tests.core.clients.resources.user_client import UserClient
from tests.core.clients.auth_session import AuthSession

from tests.core.schemas.resources.auth_schema import RegisterUserRequestSchema
from tests.core.schemas.resources.user_schema import GetUserResponseSchema, UserWithPasswordSchema

from tests.core.clients.transports.user_transport import UserTransportClient


@pytest.fixture(scope="function")
def _user_transport_client_public(httpx_client: AsyncClient) -> UserTransportClient:
    return UserTransportClient(client=httpx_client)


@pytest.fixture(scope="function")
def _user_transport_client_private(httpx_client: AsyncClient, auth_session: AuthSession) -> UserTransportClient:
    return UserTransportClient(client=httpx_client, auth=auth_session)


@pytest.fixture(scope="function")
def user_client_public(_user_transport_client_public: UserTransportClient) -> UserClient:
    return UserClient(transport=_user_transport_client_public)


@pytest.fixture(scope="function")
def user_client_private(_user_transport_client_private: UserTransportClient) -> UserClient:
    return UserClient(transport=_user_transport_client_private)


@pytest.fixture(scope="function")
def user_data_to_register() -> RegisterUserRequestSchema:
    return RegisterUserRequestSchema()


@pytest_asyncio.fixture(scope="function")
async def test_user(
    user_client_private: UserClient, user_data_to_register: RegisterUserRequestSchema
) -> GetUserResponseSchema:
    user = await user_client_private.get_me()
    user_with_password = UserWithPasswordSchema(**user.model_dump(), password=user_data_to_register.password)

    return user_with_password
