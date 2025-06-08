from fastapi import APIRouter
from controller.article_controller import article_controller

api_router = APIRouter(prefix="/api")

api_router.include_router(article_controller, prefix="/articles", tags=["Articles"])
