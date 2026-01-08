from typing import List
import allure

from tests.core.clients.transports.file_transport import FileTransportClient
from tests.core.clients.resources.base_client import BaseClient
from tests.core.schemas.resources.file_schema import (
    FileSchema,
    CreateFileRequestSchema,
    CreateFileResponseSchema,
    GetFileResponseSchema,
    UpdateFileRequestSchema,
)
from tests.core.clients.auth_session import protected
from tests.core.utils.logger import get_logger
from tests.core.schemas.api_response import APIResponseSchema
from tests.core.clients.error_handler import error_handler
from tests.api.utils.assertions.json_schema import validate_json_schema


class FileClient(BaseClient):
    def __init__(self, transport: FileTransportClient):
        super().__init__(transport)
        self._logger = get_logger("FILE CLIENT")

    @protected
    @error_handler("CREATE file")
    @allure.step("CREATE file")
    async def create(self, data: CreateFileRequestSchema, **kwargs) -> APIResponseSchema[CreateFileResponseSchema]:
        response = await self._transport.create(file=data.model_dump(), **kwargs)
        response.raise_for_status()
        validate_json_schema(response.json(), CreateFileResponseSchema.model_json_schema())
        response_data = CreateFileResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @error_handler("GET all files")
    @allure.step("GET all files")
    async def get_all(self, **kwargs) -> APIResponseSchema[List[FileSchema]]:
        response = await self._transport.get_all(**kwargs)
        response.raise_for_status()

        for item in response.json():
            validate_json_schema(item, FileSchema.model_json_schema())

        response_data = [FileSchema.model_validate(item) for item in response.json()]

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @error_handler("GET file by id")
    @allure.step("GET file by id")
    async def get(self, id: int, **kwargs) -> APIResponseSchema[GetFileResponseSchema]:
        response = await self._transport.get_one(id=id, **kwargs)
        response.raise_for_status()
        validate_json_schema(response.json(), GetFileResponseSchema.model_json_schema())
        response_data = GetFileResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @error_handler("GET file by filename")
    @allure.step("GET file by filename")
    async def get_by_filename(self, filename: str, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.get_by_filename(filename=filename, **kwargs)
        response.raise_for_status()

        return APIResponseSchema.create_success(status_code=response.status_code, binary_data=response.content)

    @protected
    @error_handler("UPDATE file by id")
    @allure.step("UPDATE file by id")
    async def update(self, id: int, data: UpdateFileRequestSchema, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.update(id=id, file=data.model_dump(), **kwargs)
        response.raise_for_status()

        return APIResponseSchema(status_code=response.status_code)

    @protected
    @error_handler("DELETE file by id")
    @allure.step("DELETE file by id")
    async def delete(self, id: int, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.delete(id=id, **kwargs)
        response.raise_for_status()

        return APIResponseSchema(status_code=response.status_code)

    @protected
    @error_handler("DELETE unused files")
    @allure.step("DELETE unused files")
    async def delete_unused(self, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.delete_all_unused(**kwargs)
        response.raise_for_status()

        return APIResponseSchema(status_code=response.status_code)
