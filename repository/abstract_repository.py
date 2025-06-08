from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all(cls):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(cls):
        raise NotImplementedError

    @abstractmethod
    async def create(cls):
        raise NotImplementedError

    @abstractmethod
    async def update(cls):
        raise NotImplementedError

    @abstractmethod
    async def delete(cls):
        raise NotImplementedError
