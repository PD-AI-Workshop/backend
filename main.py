from fastapi import FastAPI
from APIRouter import api_router
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import generate_latest
from metrics.custom_metrics import metrics_middleware, custom_registry
from fastapi.responses import Response
from script.create_admin import create_admin
from contextlib import asynccontextmanager

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_admin()
    yield

app = FastAPI(lifespan=lifespan)

Instrumentator().instrument(app).expose(app)


@app.get("/custom-metrics")
async def get_custom_metrics():
    return Response(content=generate_latest(custom_registry), media_type="text/plain")


app.middleware("http")(metrics_middleware)
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://ai-workshop.zyxel123.keenetic.name"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)


def main():
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
