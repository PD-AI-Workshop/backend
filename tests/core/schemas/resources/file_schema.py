from tests.core.schemas.base import BaseSchema


class FileSchema(BaseSchema):
    id: int
    name: str
    size: int
    url: str


class CreateFileRequestSchema(BaseSchema):
    file: bytes


class CreateFileResponseSchema(FileSchema):
    pass


class GetFileResponseSchema(FileSchema):
    pass


class UpdateFileRequestSchema(BaseSchema):
    uploaded_file: bytes
