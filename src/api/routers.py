from fastapi import APIRouter

from api.api_v1.users import users_router
from core.config import settings

api_router = APIRouter(prefix=settings.api_prefix.v1.prefix)

api_router.include_router(users_router, prefix=settings.api_prefix.v1.users, tags=["Users"])
