import pytest
from typing import List
import pytest_asyncio
from httpx import AsyncClient

from tests.core.clients.resources.user_client import UserClient
from tests.core.clients.resources.auth_client import AuthClient
from tests.core.clients.auth_session import AuthSession

from tests.core.schemas.resources.auth_schema import RegisterUserRequestSchema, LoginUserRequestSchema
from tests.core.schemas.resources.user_schema import UserWithPasswordSchema, UpdateUserRequestSchema

from tests.core.clients.transports.user_transport import UserTransportClient

from tests.config import settings


@pytest.fixture(scope="function")
def _user_transport_client_public(httpx_client: AsyncClient) -> UserTransportClient:
    return UserTransportClient(client=httpx_client)


@pytest.fixture(scope="function")
def _user_transport_client_private(httpx_client: AsyncClient, auth_session: AuthSession) -> UserTransportClient:
    return UserTransportClient(client=httpx_client, auth=auth_session)


@pytest.fixture(scope="function")
def _user_transport_client_private_admin(
    httpx_client: AsyncClient, auth_session_admin: AuthSession
) -> UserTransportClient:
    return UserTransportClient(client=httpx_client, auth=auth_session_admin)


@pytest.fixture(scope="function")
def user_client_public(_user_transport_client_public: UserTransportClient) -> UserClient:
    return UserClient(transport=_user_transport_client_public)


@pytest.fixture(scope="function")
def user_client_private(_user_transport_client_private: UserTransportClient) -> UserClient:
    return UserClient(transport=_user_transport_client_private)


@pytest.fixture(scope="function")
def user_client_private_admin(_user_transport_client_private_admin: UserTransportClient) -> UserClient:
    return UserClient(transport=_user_transport_client_private_admin)


@pytest.fixture(scope="function")
def user_data_to_register() -> RegisterUserRequestSchema:
    return RegisterUserRequestSchema()


@pytest.fixture(scope="function")
def user_data_to_update() -> UpdateUserRequestSchema:
    return UpdateUserRequestSchema()


@pytest.fixture(scope="function")
def user_data_to_login_admin() -> LoginUserRequestSchema:
    return LoginUserRequestSchema(username=settings.ADMIN.EMAIL, password=settings.ADMIN.PASSWORD)


@pytest.fixture(scope="function")
def admin_data() -> UserWithPasswordSchema:
    return UserWithPasswordSchema(
        id=settings.ADMIN.ID,
        email=settings.ADMIN.EMAIL,
        is_active=settings.ADMIN.IS_ACTIVE,
        is_superuser=settings.ADMIN.IS_SUPERUSER,
        is_verified=settings.ADMIN.IS_VERIFIED,
        password=settings.ADMIN.PASSWORD,
        username=settings.ADMIN.USERNAME,
        role=settings.ADMIN.ROLE,
    )


@pytest_asyncio.fixture(scope="function")
async def test_user(
    auth_session: AuthSession, user_data_to_register: RegisterUserRequestSchema
) -> UserWithPasswordSchema:
    user_data = auth_session.credentials.user
    return UserWithPasswordSchema(**user_data.model_dump(), password=user_data_to_register.password)


@pytest_asyncio.fixture(scope="function")
async def multiple_test_users(auth_client_public: AuthClient) -> List[UserWithPasswordSchema]:
    users_data = [RegisterUserRequestSchema() for _ in range(settings.TEST_ENTITIES_COUNT)]
    users = []

    for user in users_data:
        register_user_response = await auth_client_public.register(user)
        users.append(UserWithPasswordSchema(**register_user_response.data.model_dump(), password=user.password))

    return users
