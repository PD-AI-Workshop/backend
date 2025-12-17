import pytest
import pytest_asyncio
from httpx import AsyncClient

from tests.core.clients.resources.auth_client import AuthClient
from tests.core.clients.auth_session import AuthSession
from tests.core.clients.resources.user_client import UserClient
from tests.core.clients.transports.auth_transport import AuthTransportClient

from tests.core.schemas.resources.auth_schema import RegisterUserRequestSchema, LoginUserRequestSchema


@pytest.fixture(scope='function')
def _auth_transport_client_public(httpx_client: AsyncClient) -> AuthTransportClient:
    return AuthTransportClient(client=httpx_client)

@pytest.fixture(scope='function')
def _auth_transport_client_private(httpx_client: AsyncClient, auth_session: AuthSession) -> AuthTransportClient:
    return AuthTransportClient(client=httpx_client, auth=auth_session)

@pytest.fixture(scope='function')
def auth_client_public(_auth_transport_client_public: AuthTransportClient, user_client_public: UserClient) -> AuthClient:
    return AuthClient(transport=_auth_transport_client_public, user_client=user_client_public)

@pytest_asyncio.fixture(scope='function')
async def auth_client_private(
    auth_client_public: AuthClient,
    user_data_to_register: RegisterUserRequestSchema
) -> AuthClient:
    """Фикстура создает аутентифицированного клиента через регистрацию и логин"""

    await auth_client_public.register(user_data_to_register)

    login_data = LoginUserRequestSchema(
        username=user_data_to_register.email, 
        password=user_data_to_register.password,
    )
    await auth_client_public.login(login_data)

    return auth_client_public


@pytest.fixture(scope='function')
def auth_session(
    auth_client_private: AuthClient,
) -> AuthSession:
    """Получаем сессию аутентифицированного пользователя"""

    return auth_client_private.session