from fastapi import APIRouter, Depends, UploadFile, File, Form
from service.file_service import FileService
from dependencies.file_dependencies import get_file_service
from dto.file_dto import CreateFileDto, FileDto, UpdateFileDto


file_controller = APIRouter()


@file_controller.get("/")
async def get_all(service: FileService = Depends(get_file_service)) -> list[FileDto]:
    return await service.get_all()


@file_controller.get("/{id}")
async def get_by_id(id: int, service: FileService = Depends(get_file_service)) -> FileDto:
    return await service.get_by_id(id)


@file_controller.post("/")
async def create(
    file: UploadFile = File(...), article_id: int = Form(...), service: FileService = Depends(get_file_service)
) -> FileDto:
    return await service.create(file, article_id)


@file_controller.put("/{id}")
async def update(
    id: int,
    uploaded_file: UploadFile = File(...),
    article_id: int = Form(...),
    service: FileService = Depends(get_file_service),
) -> None:
    await service.update(id, uploaded_file, article_id)


@file_controller.delete("/{id}")
async def delete(id: int, service: FileService = Depends(get_file_service)) -> None:
    await service.delete(id)
