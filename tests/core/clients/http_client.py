from httpx import Response, AsyncClient
from typing import Optional, Callable
from functools import wraps

import allure


from tests.core.utils.logger import get_logger
from tests.core.clients.auth_session import AuthSession


logger = get_logger('HTTP_CLIENT')


def allure_http_step(method: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, endpoint: str | None = None, *args, **kwargs):
            request = f'{method} {endpoint}'

            with allure.step(request):
                if kwargs.get('params'):
                    allure.attach(str(kwargs['params']), name="Query params")
                if kwargs.get('json'):
                    allure.attach(str(kwargs['json']), name="Request body")
                if kwargs.get('headers'):
                    allure.attach(str(kwargs['headers']), name="Request headers")
                
                try:
                    response = await func(self, endpoint, *args, **kwargs)
                except Exception as e:
                    logger.error(f"{request} request is failed with error: {e}")
                    raise
                
                allure.attach(f"Status: {response.status_code}", name="Response status")
                if response.text:
                    allure.attach(response.text, name="Response body")
                
                return response
        return wrapper
    return decorator


class HTTPClient:
    def __init__(self, client: AsyncClient, auth: Optional[AuthSession] = None):
        self.client = client
        self._auth = auth

    def __prepare_headers(self, headers: dict, auth: bool) -> dict:
        headers = headers.copy() if headers else {}
        if auth and self._auth:
            headers.update(self._auth.auth_headers)
        return headers

    @allure_http_step('GET')
    async def get(
        self,
        endpoint: str | None = None,
        params: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        updated_headers = self.__prepare_headers(headers, auth)
        return await self.client.get(url=endpoint, params=params, headers=updated_headers, **kwargs)

    @allure_http_step('POST')
    async def post(
        self,
        endpoint: str | None = None,
        json: dict = {},
        files: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        updated_headers = self.__prepare_headers(headers, auth)
        return await self.client.post(url=endpoint, json=json, headers=updated_headers, files=files, **kwargs)

    @allure_http_step('PUT')
    async def put(
        self,
        endpoint: str | None = None,
        json: dict = {},
        files: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        updated_headers = self.__prepare_headers(headers, auth)
        return await self.client.put(url=endpoint, json=json, headers=updated_headers, files=files, **kwargs)

    @allure_http_step('PATCH')
    async def patch(
        self,
        endpoint: str | None = None,
        json: dict = {},
        files: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        updated_headers = self.__prepare_headers(headers, auth)
        return await self.client.patch(url=endpoint, json=json, headers=updated_headers, files=files, **kwargs)

    @allure_http_step('DELETE')
    async def delete(
        self,
        endpoint: str | None = None,
        params: dict = {},
        headers: dict = {},
        auth: bool = False,
        **kwargs,
    ) -> Response:
        updated_headers = self.__prepare_headers(headers, auth)
        return await self.client.delete(url=endpoint, params=params, headers=updated_headers, **kwargs)
