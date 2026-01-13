from idlelib.query import Query

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

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


@article_router.get("/{article_id}", response_model=ArticleRead)
async def get_artice(
    article_id: UUID,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await ArticleService.get_article(
        session=session,
        article_id=article_id,
    )


@article_router.get("/", response_model=Page[ArticleRead])
async def get_articles(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    params: Annotated[Params, Depends(Params)],
    user: Annotated[User, Depends(current_active_user)],
    search: str | None = Query(None, min_length=2),
):
    stmt = ArticleService.get_articles_stmt(search=search)
    return await paginate(session, stmt, params)
