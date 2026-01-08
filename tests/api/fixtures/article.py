import pytest
from random import choice
from typing import List
import pytest_asyncio
from httpx import AsyncClient

from tests.core.clients.resources.article_client import ArticleClient
from tests.core.clients.auth_session import AuthSession

from tests.core.schemas.resources.article_schema import (
    ArticleSchema,
    CreateArticleRequestSchema,
    UpdateArticleRequestSchema,
)
from tests.core.schemas.resources.category_schema import CategorySchema
from tests.core.schemas.resources.file_schema import FileSchema

from tests.core.clients.transports.article_transport import ArticleTransportClient


@pytest.fixture(scope="function")
def _article_transport_client_public(httpx_client: AsyncClient) -> ArticleTransportClient:
    return ArticleTransportClient(client=httpx_client)


@pytest.fixture(scope="function")
def _article_transport_client_private(httpx_client: AsyncClient, auth_session: AuthSession) -> ArticleTransportClient:
    return ArticleTransportClient(client=httpx_client, auth=auth_session)


@pytest.fixture(scope="function")
def _article_transport_client_private_writer(
    httpx_client: AsyncClient, auth_session_writer: AuthSession
) -> ArticleTransportClient:
    return ArticleTransportClient(client=httpx_client, auth=auth_session_writer)


@pytest.fixture(scope="function")
def _article_transport_client_private_admin(
    httpx_client: AsyncClient, auth_session_admin: AuthSession
) -> ArticleTransportClient:
    return ArticleTransportClient(client=httpx_client, auth=auth_session_admin)


@pytest.fixture(scope="function")
def article_client_public(_article_transport_client_public: ArticleTransportClient) -> ArticleClient:
    return ArticleClient(transport=_article_transport_client_public)


@pytest.fixture(scope="function")
def article_client_private(_article_transport_client_private: ArticleTransportClient) -> ArticleClient:
    return ArticleClient(transport=_article_transport_client_private)


@pytest.fixture(scope="function")
def article_client_private_writer(_article_transport_client_private_writer: ArticleTransportClient) -> ArticleClient:
    return ArticleClient(transport=_article_transport_client_private_writer)


@pytest.fixture(scope="function")
def article_client_private_admin(_article_transport_client_private_admin: ArticleTransportClient) -> ArticleClient:
    return ArticleClient(transport=_article_transport_client_private_admin)


@pytest.fixture(scope="function")
def article_data_to_create(test_category: CategorySchema, test_file: FileSchema) -> CreateArticleRequestSchema:
    return CreateArticleRequestSchema(
        main_image_url=test_file.url,
        category_ids=[test_category.id],
        image_ids=[test_file.id],
    )


@pytest.fixture(scope="function")
def article_data_to_update(
    multiple_test_categories: List[CategorySchema], multiple_test_files: List[FileSchema]
) -> UpdateArticleRequestSchema:
    return UpdateArticleRequestSchema(
        category_ids=[item.id for item in multiple_test_categories],
        image_ids=[item.id for item in multiple_test_files],
        main_image_url=choice(multiple_test_files).url,
    )


@pytest.fixture(scope="function")
def article_data_to_create_multiple(
    multiple_test_categories: List[CategorySchema], multiple_test_files: List[FileSchema]
) -> List[CreateArticleRequestSchema]:
    categories_ids = [item.id for item in multiple_test_categories]
    files_ids = [item.id for item in multiple_test_files]
    data = []

    for file_id in files_ids:
        data.append(
            CreateArticleRequestSchema(
                category_ids=[choice(categories_ids)],
                image_ids=[file_id],
                main_image_url=choice(multiple_test_files).url,
            )
        )

    return data


@pytest_asyncio.fixture(scope="function")
async def test_article(
    article_client_private_admin: ArticleClient,
    article_data_to_create: CreateArticleRequestSchema,
    auth_session_admin: AuthSession,
) -> ArticleSchema:
    create_article_response = await article_client_private_admin.create(article_data_to_create)
    article_dict = create_article_response.data.model_dump()
    article_dict.update({"username": auth_session_admin.credentials.user.username})

    return ArticleSchema(**article_dict)


@pytest_asyncio.fixture(scope="function")
async def multiple_test_articles(
    article_client_private_admin: ArticleClient, article_data_to_create_multiple: List[CreateArticleRequestSchema]
) -> List[ArticleSchema]:
    articles = []

    for article in article_data_to_create_multiple:
        create_article_response = await article_client_private_admin.create(article)
        articles.append(ArticleSchema(**create_article_response.data.model_dump()))

    return articles
