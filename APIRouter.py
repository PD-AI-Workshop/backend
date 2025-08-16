from fastapi import APIRouter
from auth.auth_router import auth_router
from controller.user_controller import user_router
from controller.file_controller import file_controller
from controller.article_controller import article_controller
from controller.category_controller import category_controller
from controller.health_check_controller import health_check_controller

api_router = APIRouter(prefix="/api")

api_router.include_router(article_controller, prefix="/articles", tags=["Articles"])
api_router.include_router(category_controller, prefix="/categories", tags=["Categories"])
api_router.include_router(file_controller, prefix="/files", tags=["Files"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(health_check_controller, prefix="/health", tags=["health"])
