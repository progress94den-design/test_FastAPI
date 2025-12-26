import uvicorn

from fastapi import FastAPI

from api import api_router
from core.config import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.api_prefix.prefix)

if __name__ == '__main__':
    uvicorn.run(
        "main.app",
        host=settings.run_server.host,
        port=settings.run_server.port,
        reload=True
    )
