from minio import S3Error
from sqlalchemy import select
from settings import settings
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from db.session import async_session_maker

import asyncio

health_check_controller = APIRouter()


async def check_postgres():
    async with async_session_maker() as session:
        query = select(1)
        result = await session.execute(query)
        return result.scalar_one() == 1


async def check_minio():
    try:
        settings.client.list_buckets()
        return True
    except S3Error:
        return True
    except Exception:
        return False


async def check_redis():
    try:
        return settings.redis_client.ping()
    except Exception:
        return False


@asynccontextmanager
async def timeout_manager(timeout: float = 2.0):
    try:
        yield await asyncio.wait_for(asyncio.sleep(0), timeout=timeout)
    except asyncio.TimeoutError:
        pass


@health_check_controller.get("/")
async def health_check() -> JSONResponse:
    services = {"postgres": check_postgres, "minio": check_minio, "redis": check_redis}

    tasks = {name: asyncio.create_task(checker()) for name, checker in services.items()}
    results = {}
    status = "ok"

    for name, task in tasks.items():
        try:
            results[name] = await asyncio.wait_for(task, timeout=2.0)
            if not results[name]:
                status = "error"
        except (asyncio.TimeoutError, Exception):
            results[name] = False
            status = "error"

    http_status = 200 if status == "ok" else 503

    return JSONResponse(content={"status": status, "services": results}, status_code=http_status)
