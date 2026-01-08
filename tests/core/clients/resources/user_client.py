from typing import List
import allure

from tests.core.clients.transports.user_transport import UserTransportClient
from tests.core.clients.resources.base_client import BaseClient
from tests.core.schemas.resources.user_schema import (
    UserSchema,
    GetUserResponseSchema,
    UpdateUserRequestSchema,
    UpdateUserResponseSchema,
)
from tests.core.clients.auth_session import protected
from tests.core.clients.error_handler import error_handler
from tests.core.utils.logger import get_logger

from tests.core.schemas.api_response import APIResponseSchema
from tests.api.utils.assertions.json_schema import validate_json_schema


class UserClient(BaseClient):
    def __init__(self, transport: UserTransportClient):
        super().__init__(transport)
        self._logger = get_logger("USER CLIENT")

    @protected
    @error_handler("GET all users")
    @allure.step("GET all users")
    async def get_all(self, **kwargs) -> APIResponseSchema[List[UserSchema]]:
        response = await self._transport.get_all(**kwargs)
        response.raise_for_status()

        for item in response.json():
            validate_json_schema(item, UserSchema.model_json_schema())

        response_data = [UserSchema.model_validate(item) for item in response.json()]

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @protected
    @error_handler("GET user by id")
    @allure.step("GET user by id")
    async def get(self, id: int, **kwargs) -> APIResponseSchema[GetUserResponseSchema]:
        response = await self._transport.get_one(id=id, **kwargs)
        response.raise_for_status()
        validate_json_schema(response.json(), GetUserResponseSchema.model_json_schema())
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @protected
    @error_handler("GET current user")
    @allure.step("GET current user")
    async def get_me(self, **kwargs) -> APIResponseSchema[GetUserResponseSchema]:
        response = await self._transport.get_me(**kwargs)
        response.raise_for_status()
        validate_json_schema(response.json(), GetUserResponseSchema.model_json_schema())
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @protected
    @error_handler("UPDATE user by id")
    @allure.step("UPDATE user by id")
    async def update(
        self, id: int, data: UpdateUserRequestSchema, **kwargs
    ) -> APIResponseSchema[UpdateUserResponseSchema]:
        response = await self._transport.update(id=id, json=data.model_dump(), **kwargs)
        response.raise_for_status()
        validate_json_schema(response.json(), UpdateUserResponseSchema.model_json_schema())
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @protected
    @error_handler("UPDATE current user")
    @allure.step("UPDATE current user")
    async def update_me(self, data: UpdateUserRequestSchema, **kwargs) -> APIResponseSchema[UpdateUserResponseSchema]:
        response = await self._transport.update_me(json=data.model_dump(), **kwargs)
        response.raise_for_status()
        validate_json_schema(response.json(), UpdateUserResponseSchema.model_json_schema())
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @protected
    @error_handler("DELETE user by id")
    @allure.step("DELETE user by id")
    async def delete(self, id: int, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.delete(id=id, **kwargs)
        response.raise_for_status()

        return APIResponseSchema.create_success(status_code=response.status_code)
