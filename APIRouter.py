from fastapi import APIRouter
from controller.file_controller import file_controller
from controller.article_controller import article_controller
from controller.category_controller import category_controller

api_router = APIRouter(prefix="/api")

api_router.include_router(article_controller, prefix="/articles", tags=["Articles"])
api_router.include_router(category_controller, prefix="/categories", tags=["Categories"])
api_router.include_router(file_controller, prefix="/files", tags=["Files"])
