import pytest
from typing import List
import pytest_asyncio
from httpx import AsyncClient

from tests.core.clients.resources.category_client import CategoryClient
from tests.core.clients.auth_session import AuthSession

from tests.core.schemas.resources.category_schema import CreateCategoryRequestSchema, UpdateCategoryRequestSchema, CategorySchema
from tests.core.clients.transports.category_transport import CategoryTransportClient

from tests.config import settings


@pytest.fixture(scope="function")
def _category_transport_client_public(httpx_client: AsyncClient) -> CategoryTransportClient:
    return CategoryTransportClient(client=httpx_client)


@pytest.fixture(scope="function")
def _category_transport_client_private(httpx_client: AsyncClient, auth_session: AuthSession) -> CategoryTransportClient:
    return CategoryTransportClient(client=httpx_client, auth=auth_session)


@pytest.fixture(scope="function")
def _category_transport_client_private_admin(httpx_client: AsyncClient, auth_session_admin: AuthSession) -> CategoryTransportClient:
    return CategoryTransportClient(client=httpx_client, auth=auth_session_admin)


@pytest.fixture(scope="function")
def category_client_public(_category_transport_client_public: CategoryTransportClient) -> CategoryClient:
    return CategoryClient(transport=_category_transport_client_public)


@pytest.fixture(scope="function")
def category_client_private(_category_transport_client_private: CategoryTransportClient) -> CategoryClient:
    return CategoryClient(transport=_category_transport_client_private)


@pytest.fixture(scope="function")
def category_client_private_admin(_category_transport_client_private_admin: CategoryTransportClient) -> CategoryClient:
    return CategoryClient(transport=_category_transport_client_private_admin)


@pytest.fixture(scope="function")
def category_data_to_create() -> CreateCategoryRequestSchema:
    return CreateCategoryRequestSchema()


@pytest.fixture(scope="function")
def category_data_to_update() -> UpdateCategoryRequestSchema:
    return UpdateCategoryRequestSchema()


@pytest_asyncio.fixture(scope="function")
async def test_category(category_client_private_admin: CategoryClient, category_data_to_create: CreateCategoryRequestSchema) -> CategorySchema:
    create_category_response = await category_client_private_admin.create(category_data_to_create)
    return CategorySchema(**create_category_response.data.model_dump())


@pytest_asyncio.fixture(scope="function")
async def multiple_test_categories(category_client_private_admin: CategoryClient) -> List[CategorySchema]:
    categories_data = [CreateCategoryRequestSchema() for _ in range(settings.TEST_ENTITIES_COUNT)]
    categories = []

    for category in categories_data:
        create_category_response = await category_client_private_admin.create(category)
        categories.append(CategorySchema(**create_category_response.data.model_dump()))

    return categories
