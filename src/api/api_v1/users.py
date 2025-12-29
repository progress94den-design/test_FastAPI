from fastapi import APIRouter

from api.dependencies.authentication.fastapi_users_routers import fastapi_users
from schemas.user import UserRead, UserUpdate

users_router = APIRouter()

# /me
# /{id} - GET, PATCH, DELETE доступен только для СуперЮзера. Создание СуперЮзера пока не реализованно
users_router.include_router(
    router=fastapi_users.get_users_router(UserRead, UserUpdate),
)
