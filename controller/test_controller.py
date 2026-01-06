from fastapi import APIRouter, Depends
from dependencies.test_dependencies import get_test_service
from service.test_service import TestService
from dependencies.role_dependencies import admin_dependency

test_controller = APIRouter()


@test_controller.delete("/database", dependencies=admin_dependency)
async def cleanup_test_db(service: TestService = Depends(get_test_service)) -> dict:
    await service.cleanup_test_db()
    return {'message': 'testing database was successfully cleaned up'}


