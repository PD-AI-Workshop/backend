from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class BaseDTOFactory(Generic[T]):
    @classmethod
    def dto_list(cls, count: int = 2, **common_overrides) -> list[T]:
        return [cls.dto(**common_overrides) for _ in range(count)]
