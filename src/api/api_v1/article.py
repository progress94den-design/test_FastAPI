from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from core.db_helper import db_helper
from schemas.article import ArticleCreate, ArticleRead
from models.users import User
from api.dependencies.authentication.fastapi_users_routers import current_active_user
from services.article import ArticleService

article_router = APIRouter()


@article_router.post("/", response_model=ArticleRead)
async def create_article(
    data: Annotated[ArticleCreate, Depends(ArticleCreate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await ArticleService.create_article(
        data=data,
        session=session,
        user=user,
    )
