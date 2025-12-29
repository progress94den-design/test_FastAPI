from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.get("/")
async def index():
    return {"message": "Hello World"}
