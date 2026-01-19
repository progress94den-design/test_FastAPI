from fastapi import APIRouter, Depends, Query, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from core.db_helper import db_helper
from schemas.article import (
    ArticleCreate,
    ArticleRead,
    ArticleUpdate,
    ArticleCategoriesUpdate,
)
from models.users import User
from api.dependencies.authentication.fastapi_users_routers import current_active_user
from services.article import article_service

article_router = APIRouter()


@article_router.post(
    "/",
    response_model=ArticleRead,
    summary="Create a new article",
    description="Creates a new article in the system. "
    "Supports optional image upload. "
    "Requires authentication. Returns the created article.",
)
async def create_article(
    data: Annotated[ArticleCreate, Depends(ArticleCreate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
    image: UploadFile | None = File(None),
):
    """
    Creates a new article.

    - **data**: ArticleCreate schema containing 'title', 'text'.
    - **session**: Async database session.
    - **user**: Authenticated current user.
    - **image**: Optional image file.

    Returns the created article as ArticleCreate schema.
    """
    return await article_service.create_article(
        data=data,
        session=session,
        user=user,
        image=image,
    )


@article_router.get(
    "/{article_id}",
    response_model=ArticleRead,
    summary="Get article by ID",
    description="Fetches a single article by its UUID. "
    "Requires authentication. Returns ArticleRead schema.",
)
async def get_article(
    article_id: UUID,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
):
    """
    Retrieve an article by its unique identifier.

    - **article_id**: UUID of the article.
    - **session**: Async database session.
    - **user**: Authenticated current user.

    Returns the article matching the given ID.
    """
    return await article_service.get_article(
        session=session,
        article_id=article_id,
    )


@article_router.get(
    "/",
    response_model=Page[ArticleRead],
    summary="List articles with pagination",
    description="Returns a paginated list of articles. "
    "Supports query parameters for pagination. "
    "Supports search by title/text and filtering by category. "
    "Requires authentication.",
)
async def get_articles(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    params: Annotated[Params, Depends(Params)],
    user: Annotated[User, Depends(current_active_user)],
    search: str | None = Query(
        None, min_length=2, description="Search query for title or text"
    ),
    category_id: UUID | None = Query(None, description="Filter by category UUID"),
):
    """
    Get a paginated list of articles.

    - **session**: Async database session.
    - **params**: Pagination parameters (page, size).
    - **user**: Authenticated current user.
    - **search**: Optional search string for title/text.
    - **category_id**: Optional category UUID to filter articles.

    Returns a paginated list of ArticleRead objects.
    """
    stmt = article_service.get_articles_stmt(search=search, category_id=category_id)
    return await paginate(session, stmt, params)


@article_router.patch(
    "/{article_id}",
    response_model=ArticleRead,
    summary="Update an article",
    description="Updates an existing article by UUID. "
    "Supports updating content and optionally the image. "
    "Requires authentication.",
)
async def update_article(
    article_id: UUID,
    data: Annotated[ArticleUpdate, Depends(ArticleUpdate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
    image: UploadFile | None = File(None),
):
    """
    Update an existing article.

    - **article_id**: UUID of the article.
    - **data**: ArticleUpdate schema with fields to update.
    - **session**: Async database session.
    - **user**: Authenticated current user.
    - **image**: Optional image file.

    Returns the updated article.
    """
    return await article_service.update_article(
        article_id=article_id,
        data=data,
        session=session,
        user=user,
        image=image,
    )


@article_router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an article",
    description="Fake deletion of an article by UUID. "
    "Deletes the article from the Article and moves it to DeletedArticle. "
    "Requires authentication. "
    "Returns no content.",
)
async def delete_article(
    article_id: UUID,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
):
    """
    Fake deletion an article by its UUID.

    - **article_id**: UUID of the article.
    - **session**: Async database session.
    - **user**: Authenticated current user.

    Returns HTTP 204 No Content on success.
    """
    return await article_service.delete_article(
        article_id=article_id,
        session=session,
        user=user,
    )


@article_router.put(
    "/{article_id}/categories",
    response_model=ArticleRead,
    summary="Set categories for an article",
    description="Assigns one or more categories to an article. "
    "Requires authentication. "
    "Returns the updated article.",
)
async def set_article_categories(
    article_id: UUID,
    data: Annotated[ArticleCategoriesUpdate, Depends(ArticleCategoriesUpdate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
):
    """
    Set categories for an article.

    - **article_id**: UUID of the article.
    - **data**: ArticleCategoriesUpdate schema with list of category UUIDs.
    - **session**: Async database session.
    - **user**: Authenticated current user.

    Returns the updated article with assigned categories.
    """
    return await article_service.set_categories(
        session=session,
        article_id=article_id,
        category_ids=data.category_ids,
        user=user,
    )
