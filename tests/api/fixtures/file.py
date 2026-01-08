import pytest
from typing import List
import pytest_asyncio
from httpx import AsyncClient

from tests.core.clients.resources.file_client import FileClient
from tests.core.clients.auth_session import AuthSession

from tests.core.schemas.resources.file_schema import (
    FileSchema,
    CreateFileRequestSchema,
    UpdateFileRequestSchema,
)
from tests.core.clients.transports.file_transport import FileTransportClient


def get_file_data(filename: str) -> bytes:
    with open(f"./tests/core/data/static/{filename}", "rb") as file:
        return file.read()


@pytest.fixture(scope="function")
def _file_transport_client_public(httpx_client: AsyncClient) -> FileTransportClient:
    return FileTransportClient(client=httpx_client)


@pytest.fixture(scope="function")
def _file_transport_client_private(httpx_client: AsyncClient, auth_session: AuthSession) -> FileTransportClient:
    return FileTransportClient(client=httpx_client, auth=auth_session)


@pytest.fixture(scope="function")
def _file_transport_client_private_admin(
    httpx_client: AsyncClient, auth_session_admin: AuthSession
) -> FileTransportClient:
    return FileTransportClient(client=httpx_client, auth=auth_session_admin)


@pytest.fixture(scope="function")
def _file_transport_client_private_writer(
    httpx_client: AsyncClient, auth_session_writer: AuthSession
) -> FileTransportClient:
    return FileTransportClient(client=httpx_client, auth=auth_session_writer)


@pytest.fixture(scope="function")
def file_client_public(_file_transport_client_public: FileTransportClient) -> FileClient:
    return FileClient(transport=_file_transport_client_public)


@pytest.fixture(scope="function")
def file_client_private(_file_transport_client_private: FileTransportClient) -> FileClient:
    return FileClient(transport=_file_transport_client_private)


@pytest.fixture(scope="function")
def file_client_private_admin(_file_transport_client_private_admin: FileTransportClient) -> FileClient:
    return FileClient(transport=_file_transport_client_private_admin)


@pytest.fixture(scope="function")
def file_client_private_writer(_file_transport_client_private_writer: FileTransportClient) -> FileClient:
    return FileClient(transport=_file_transport_client_private_writer)


@pytest.fixture(scope="function")
def file_data_to_create() -> CreateFileRequestSchema:
    file_content = get_file_data("image.png")
    return CreateFileRequestSchema(file=file_content)


@pytest.fixture(scope="function")
def file_data_to_update() -> UpdateFileRequestSchema:
    file_content = get_file_data("image2.webp")
    return UpdateFileRequestSchema(uploaded_file=file_content)


@pytest_asyncio.fixture(scope="function")
async def test_file(file_client_private_admin: FileClient, file_data_to_create: CreateFileRequestSchema) -> FileSchema:
    create_file_response = await file_client_private_admin.create(file_data_to_create)
    return FileSchema(**create_file_response.data.model_dump())


@pytest_asyncio.fixture(scope="function")
async def multiple_test_files(file_client_private_admin: FileClient) -> List[FileSchema]:
    files_data, files = [], []
    files_data.append(CreateFileRequestSchema(file=get_file_data("image.png")))
    files_data.append(CreateFileRequestSchema(file=get_file_data("image2.webp")))

    for file in files_data:
        create_file_response = await file_client_private_admin.create(file)
        files.append(FileSchema(**create_file_response.data.model_dump()))

    return files
