from sqlalchemy.ext.asyncio import AsyncSession

from model.file import File
from repository.crud_base_repository import CRUDBaseRepository


class FileRepository(CRUDBaseRepository):
    model = File

    def __init__(self, session: AsyncSession):
        super().__init__(session)
