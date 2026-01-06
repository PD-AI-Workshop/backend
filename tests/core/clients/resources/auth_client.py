from typing import Optional

from tests.core.clients.transports.auth_transport import AuthTransportClient
from tests.core.schemas.resources.auth_schema import (
    RegisterUserRequestSchema,
    RegisterUserResponseSchema,
    LoginUserRequestSchema,
    LoginUserResponseSchema,
)
from tests.core.schemas.resources.user_schema import UserSchema, GetUserResponseSchema
from tests.core.clients.resources.user_client import UserClient
from tests.core.exceptions.auth import NoAuthSessionException
from tests.core.clients.auth_session import AuthSession, LoggedInUserData, protected
from tests.core.schemas.api_response import APIResponseSchema
from tests.core.clients.resources.base_client import BaseClient

from tests.core.utils.logger import get_logger
from tests.core.clients.error_handler import error_handler


class AuthClient(BaseClient):
    """
    Клиент используется для запросов, а также для хранения сессии аутентифицированного пользователя
    """

    def __init__(self, transport: AuthTransportClient, user_client: UserClient):
        super().__init__(transport)
        self.__user_client: UserClient = user_client
        self.__session: Optional[AuthSession] = None
        self._logger = get_logger("Auth client")

    @staticmethod
    def get_login_headers() -> dict:
        return {
            "Content-Type": "application/x-www-form-urlencoded",
        }

    @staticmethod
    def get_auth_headers(token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    @error_handler("registration")
    async def register(
        self, data: RegisterUserRequestSchema, **kwargs
    ) -> APIResponseSchema[RegisterUserResponseSchema]:
        response = await self._transport.register(json=data.model_dump(), **kwargs)
        response.raise_for_status()
        response_data = RegisterUserResponseSchema.model_validate_json(response.text)

        self._logger.info(f"User registered successfully: {data.email}")
        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @error_handler("login")
    async def login(self, data: LoginUserRequestSchema, **kwargs) -> APIResponseSchema[LoginUserResponseSchema]:
        response = await self._transport.login(data=data.model_dump(), headers=self.get_login_headers(), **kwargs)
        response.raise_for_status()

        response_data = LoginUserResponseSchema.model_validate_json(response.text)

        get_user_response = await self.__user_client.get_me(headers=self.get_auth_headers(response_data.access_token))

        self.__create_session(get_user_response.data, response_data)

        self._logger.info(f"User logged in successfully: {get_user_response.data.email}")
        return APIResponseSchema.create_success(response_data, status_code=response.status_code)

    @protected
    @error_handler("logout")
    async def logout(self, **kwargs) -> APIResponseSchema[None]:
        response = await self._transport.logout(**kwargs)
        response.raise_for_status()

        if self.__session:
            self._logger.info(f"User logged out: {self.__session.credentials.user.email}")
            self.__session = None

        return APIResponseSchema.create_success(status_code=response.status_code)

    @property
    def session(self) -> AuthSession:
        if self.__session:
            return self.__session
        raise NoAuthSessionException

    def __create_session(self, user_data: GetUserResponseSchema, login_data: LoginUserResponseSchema) -> None:
        logged_in_user = LoggedInUserData(user=UserSchema.model_validate(user_data), token=login_data.access_token)
        self.__session = AuthSession(credentials=logged_in_user)
