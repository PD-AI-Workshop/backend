from httpx import Response, AsyncClient
from typing import Optional

from tests.core.utils.logger import logger
from tests.core.clients.auth_session import AuthSession

class HTTPClient:
    def __init__(self, client: AsyncClient, auth: Optional[AuthSession] = None):
        self.client = client
        self._auth = auth

    def __prepare_headers(self, headers: dict, auth: bool) -> dict:
        headers = headers.copy() if headers else {}
        if auth and self._auth:
            headers.update(self._auth.auth_headers)
        return headers

    async def get(
        self,
        endpoint: str | None = None,
        params: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        try:
            updated_headers = self.__prepare_headers(headers, auth)
            return await self.client.get(url=endpoint, params=params, headers=updated_headers, **kwargs)
        except Exception as e:
            logger.error(f"GET http-request is failed with error: {e}")
            raise

    async def post(
        self,
        endpoint: str | None = None,
        json: dict = {},
        files: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        try:
            updated_headers = self.__prepare_headers(headers, auth)
            return await self.client.post(url=endpoint, json=json, headers=updated_headers, files=files, **kwargs)
        except Exception as e:
            logger.error(f"POST http-request is failed with error: {e}")
            raise

    async def put(
        self,
        endpoint: str | None = None,
        json: dict = {},
        files: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        try:
            updated_headers = self.__prepare_headers(headers, auth)
            return await self.client.put(url=endpoint, json=json, headers=updated_headers, files=files, **kwargs)
        except Exception as e:
            logger.error(f"POST http-request is failed with error: {e}")
            raise

    async def patch(
        self,
        endpoint: str | None = None,
        json: dict = {},
        files: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        try:
            updated_headers = self.__prepare_headers(headers, auth)
            return await self.client.patch(url=endpoint, json=json, headers=updated_headers, files=files, **kwargs)
        except Exception as e:
            logger.error(f"PATCH http-request is failed with error: {e}")
            raise

    async def delete(
        self,
        endpoint: str | None = None,
        params: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        try:
            updated_headers = self.__prepare_headers(headers, auth)
            return await self.client.delete(url=endpoint, params=params, headers=updated_headers, **kwargs)
        except Exception as e:
            logger.error(f"DELETE http-request is failed with error: {e}")
            raise
