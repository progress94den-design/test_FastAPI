from fastapi import APIRouter

from api.dependencies.authentication.fastapi_users_routers import fastapi_users
from api.dependencies.authentication.auth_backend import authentication_backend
from schemas.user import UserRead, UserCreate

auth_router = APIRouter()

# /login
# /logout
auth_router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend),
)

# /register
auth_router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)
