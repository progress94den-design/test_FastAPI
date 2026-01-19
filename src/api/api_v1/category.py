from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from core.db_helper import db_helper
from schemas.category import CategoryCreate, CategoryRead
from models.users import User
from api.dependencies.authentication.fastapi_users_routers import current_active_user
from services.category import category_service

category_router = APIRouter()


@category_router.post(
    "/",
    response_model=CategoryRead,
    summary="Create a new category",
    description="Creates a new category in the system. "
    "Requires authentication. Returns the created category.",
)
async def create_category(
    data: Annotated[CategoryCreate, Depends(CategoryCreate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
):
    """
    Creates a new category.

    - **data**: CategoryCreate schema containing 'name'.
    - **session**: Async database session.
    - **user**: Authenticated current user.

    Returns the created category as CategoryRead schema.
    """
    return await category_service.create_category(
        data=data,
        session=session,
    )


@category_router.get(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Get category by ID",
    description="Fetches a single category by its UUID. "
    "Requires authentication. Returns CategoryRead schema.",
)
async def get_category(
    category_id: UUID,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
):
    """
    Retrieve a category by its unique identifier.

    - **category_id**: UUID of the category.
    - **session**: Async database session.
    - **user**: Authenticated current user.

    Returns the category matching the given ID.
    """
    return await category_service.get_category(
        session=session,
        category_id=category_id,
    )


@category_router.get(
    "/",
    response_model=Page[CategoryRead],
    summary="List categories with pagination",
    description="Returns a paginated list of categories. "
    "Supports query parameters for pagination. "
    "Requires authentication.",
)
async def get_categories(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    params: Annotated[Params, Depends(Params)],
    user: Annotated[User, Depends(current_active_user)],
):
    """
    Get a paginated list of categories.

    - **params**: Pagination parameters (page, size).
    - **session**: Async database session.
    - **user**: Authenticated current user.

    Returns a paginated list of CategoryRead objects.
    """
    stmt = category_service.get_categories_smtp()
    return await paginate(session, stmt, params)
