from fastapi import APIRouter

from core.config import settings
from api.api_v1.users import users_router
from api.api_v1.auth import auth_router
from api.api_v1.article import article_router

api_router = APIRouter(prefix=settings.api_prefix.v1.prefix)

api_router.include_router(
    users_router,
    prefix=settings.api_prefix.v1.users,
    tags=["Users"],
)
api_router.include_router(
    auth_router,
    prefix=settings.api_prefix.v1.auth,
    tags=["Auth"],
)
api_router.include_router(
    article_router,
    prefix=settings.api_prefix.v1.article,
    tags=["Article"],
)
