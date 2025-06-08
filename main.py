from fastapi import FastAPI
from APIRouter import api_router

import uvicorn

app = FastAPI()

app.include_router(api_router)


def main():
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
