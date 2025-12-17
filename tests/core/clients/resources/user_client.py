from typing import List

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


class UserClient(BaseClient):
    def __init__(self, transport: UserTransportClient):
        super().__init__(transport)
        self._logger = get_logger("User client")

    @protected
    @error_handler("get all users")
    async def get_all(self, **kwargs) -> APIResponseSchema[List[UserSchema]]:
        response = await self._transport.get_all(**kwargs)
        response.response.raise_for_status()
        response_data = [UserSchema.model_validate(item) for item in response.json()]

        return APIResponseSchema.create_success(response_data, response.status_code)

    @protected
    @error_handler("get user by id")
    async def get(self, id: int, **kwargs) -> APIResponseSchema[GetUserResponseSchema]:
        response = await self._transport.get(id=id, **kwargs)
        response.response.raise_for_status()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, response.status_code)

    @protected
    @error_handler("get current user")
    async def get_me(self, **kwargs) -> APIResponseSchema[GetUserResponseSchema]:
        response = await self._transport.get_me(**kwargs)
        response.response.raise_for_status()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        return APIResponseSchema.create_success(response_data, response.status_code)

    @protected
    @error_handler("update user by id")
    async def update(
        self, id: int, data: UpdateUserRequestSchema, **kwargs
    ) -> APIResponseSchema[UpdateUserResponseSchema]:
        response = await self._transport.update(id=id, json=data.model_dump(), **kwargs)
        response.response.raise_for_status()

        return UpdateUserResponseSchema.model_validate_json(response.text)

    @protected
    @error_handler("update current user")
    async def update_me(self, data: UpdateUserRequestSchema, **kwargs) -> APIResponseSchema[UpdateUserResponseSchema]:
        response = await self._transport.update(json=data.model_dump(), **kwargs)
        response.response.raise_for_status()

        return UpdateUserResponseSchema.model_validate_json(response.text)

    @protected
    @error_handler("delete user by id")
    async def delete(self, id: int, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.remove(id=id, **kwargs)
        response.response.raise_for_status()

        return response
