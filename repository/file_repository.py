from model.file import File
from repository.crud_base_repository import CRUDBaseRepository


class FileRepository(CRUDBaseRepository):
    model = File
