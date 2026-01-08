import pytest
import pytest_asyncio
from httpx import AsyncClient

from tests.core.clients.resources.auth_client import AuthClient
from tests.core.clients.auth_session import AuthSession
from tests.core.clients.resources.user_client import UserClient
from tests.core.clients.transports.auth_transport import AuthTransportClient

from tests.core.schemas.resources.auth_schema import (
    RegisterUserRequestSchema,
    LoginUserRequestSchema,
    RegisterUserResponseSchema,
)


@pytest.fixture(scope="function")
def _auth_transport_client_public(httpx_client: AsyncClient) -> AuthTransportClient:
    return AuthTransportClient(client=httpx_client)


@pytest.fixture(scope="function")
def _auth_transport_client_private(httpx_client: AsyncClient, auth_session: AuthSession) -> AuthTransportClient:
    return AuthTransportClient(client=httpx_client, auth=auth_session)


@pytest_asyncio.fixture(scope="function")
async def register_test_user(
    auth_client_public: AuthClient, user_data_to_register: RegisterUserRequestSchema
) -> RegisterUserResponseSchema:
    response = await auth_client_public.register(user_data_to_register)

    return response.data


@pytest_asyncio.fixture(scope="function")
async def register_test_user_writer(
    auth_client_public: AuthClient, user_data_to_register_writer: RegisterUserRequestSchema
) -> RegisterUserResponseSchema:
    response = await auth_client_public.register(user_data_to_register_writer)

    return response.data


@pytest.fixture(scope="function")
def auth_client_public(
    _auth_transport_client_public: AuthTransportClient, user_client_public: UserClient
) -> AuthClient:
    return AuthClient(transport=_auth_transport_client_public, user_client=user_client_public)


@pytest_asyncio.fixture(scope="function")
async def auth_client_private(
    register_test_user: RegisterUserResponseSchema,
    auth_client_public: AuthClient,
    user_data_to_register: RegisterUserRequestSchema,
) -> AuthClient:
    """Фикстура создает аутентифицированного клиента через регистрацию и логин"""
    login_data = LoginUserRequestSchema(
        username=user_data_to_register.email,
        password=user_data_to_register.password,
    )
    await auth_client_public.login(login_data)

    auth_session = auth_client_public.session
    auth_client_public.make_private(auth_session)

    return auth_client_public


@pytest_asyncio.fixture(scope="function")
async def auth_client_private_writer(
    register_test_user_writer: RegisterUserResponseSchema,
    auth_client_public: AuthClient,
    user_data_to_register: RegisterUserRequestSchema,
) -> AuthClient:
    """Фикстура создает аутентифицированного клиента (Писатель)"""
    login_data = LoginUserRequestSchema(
        username=user_data_to_register.email,
        password=user_data_to_register.password,
    )
    await auth_client_public.login(login_data)

    auth_session = auth_client_public.session
    auth_client_public.make_private(auth_session)

    return auth_client_public


@pytest_asyncio.fixture(scope="function")
async def auth_client_private_admin(
    auth_client_public: AuthClient, user_data_to_login_admin: LoginUserRequestSchema
) -> AuthClient:
    """Фикстура создает аутентифицированного клиента (Админа)"""
    await auth_client_public.login(user_data_to_login_admin)

    auth_session = auth_client_public.session
    auth_client_public.make_private(auth_session)

    return auth_client_public


@pytest.fixture(scope="function")
def auth_session(
    auth_client_private: AuthClient,
) -> AuthSession:
    """Получаем сессию аутентифицированного пользователя"""

    return auth_client_private.session


@pytest.fixture(scope="function")
def auth_session_writer(
    auth_client_private_admin: AuthClient,
) -> AuthSession:
    """Получаем сессию аутентифицированного пользователя(админа)"""

    return auth_client_private_admin.session


@pytest.fixture(scope="function")
def auth_session_admin(
    auth_client_private_admin: AuthClient,
) -> AuthSession:
    """Получаем сессию аутентифицированного пользователя(админа)"""

    return auth_client_private_admin.session
