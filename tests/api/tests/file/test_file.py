import pytest
from typing import List

from tests.api.utils.allure.setup import (
    allure_class_setup,
    allure_test_setup,
    Severity,
    Epic,
    Feature,
    Tag,
    Story,
)

from tests.core.clients.resources.file_client import FileClient
from tests.core.schemas.resources.file_schema import FileSchema, UpdateFileRequestSchema, CreateFileRequestSchema

from tests.api.utils.assertions.file import (
    assert_get_all_response,
    assert_delete_by_id_response,
    assert_get_by_id_response,
    assert_update_by_id_response,
    assert_create_response,
    assert_get_by_filename_response,
    assert_delete_unused_response,
)


@pytest.mark.asyncio
@pytest.mark.api
@pytest.mark.file
@allure_class_setup(
    severity=Severity.MAJOR,
    tags=[Tag.SMOKE, Tag.REGRESS],
    epic=Epic.ARTICLE_SERVICE,
    feature=Feature.FILE,
)
class TestFilePositive:
    @allure_test_setup(title="Get all files", story=Story.GET)
    async def test_get_all(self, file_client_public: FileClient, multiple_test_files: List[FileSchema]):
        get_all_files_response = await file_client_public.get_all()

        assert_get_all_response(get_all_files_response, multiple_test_files)

    @allure_test_setup(title="Get file by id", story=Story.GET)
    async def test_get_by_id(self, file_client_public: FileClient, test_file: FileSchema):
        get_file_response = await file_client_public.get(id=test_file.id)

        assert_get_by_id_response(get_file_response, test_file)

    @allure_test_setup(title="Get file by filename", story=Story.GET)
    async def test_get_by_filename(self, file_client_public: FileClient, test_file: FileSchema):
        image_uuid = test_file.url[test_file.url.rfind("/") + 1 :]
        get_file_response = await file_client_public.get_by_filename(filename=image_uuid)

        assert_get_by_filename_response(get_file_response)

    @allure_test_setup(title="Create file", story=Story.CREATE)
    async def test_create_file(
        self, file_client_private_admin: FileClient, file_data_to_create: CreateFileRequestSchema
    ):
        create_file_response = await file_client_private_admin.create(file_data_to_create)

        assert_create_response(create_file_response)

    @allure_test_setup(title="Update file by id", story=Story.UPDATE)
    async def test_update_by_id(
        self, file_client_private_admin: FileClient, test_file: FileSchema, file_data_to_update: UpdateFileRequestSchema
    ):
        update_file_response = await file_client_private_admin.update(id=test_file.id, data=file_data_to_update)

        assert_update_by_id_response(update_file_response)

    @allure_test_setup(title="Delete file by id", story=Story.DELETE)
    async def test_delete_by_id(self, file_client_private_admin: FileClient, test_file: FileSchema):
        delete_file_response = await file_client_private_admin.delete(id=test_file.id)

        assert_delete_by_id_response(delete_file_response)

    @allure_test_setup(title="Delete unused files", story=Story.DELETE)
    async def test_delete_unused(self, file_client_private_admin: FileClient, multiple_test_files: List[FileSchema]):
        delete_unused_files_response = await file_client_private_admin.delete_unused()

        assert_delete_unused_response(delete_unused_files_response)
