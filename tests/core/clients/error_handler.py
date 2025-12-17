from typing import Callable, ParamSpec, TypeVar
from functools import wraps
from pydantic import ValidationError
import httpx


P = ParamSpec("P")
R = TypeVar("R")


def error_handler(action: str):
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> R:
            try:
                return await func(self, *args, **kwargs)
            except httpx.HTTPStatusError as e:
                self._logger.error(f"HTTP error during {action}: {e}")
                status_code = e.response.status_code if e.response else 500
                return self._create_error_response(str(e), status_code)
            except ValidationError as e:
                self._logger.error(f"Response validation error during {action}: {e}")
                return self._create_error_response(f"Invalid response format: {e}", 500)
            except Exception as e:
                self._logger.error(f"Unexpected error during {action}: {e}")
                return self._create_error_response(str(e), 500)
        return wrapper
    return decorator