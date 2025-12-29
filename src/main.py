import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routers import api_router
from core.config import settings
from core.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(api_router, prefix=settings.api_prefix.prefix)

if __name__ == '__main__':
    uvicorn.run(
        "main:main_app",
        host=settings.run_server.host,
        port=settings.run_server.port,
        reload=True
    )
