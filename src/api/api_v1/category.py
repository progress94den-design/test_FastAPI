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


@category_router.post("/", response_model=CategoryRead)
async def create_category(
    data: Annotated[CategoryCreate, Depends(CategoryCreate)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await category_service.create_category(
        data=data,
        session=session,
    )


@category_router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: UUID,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await category_service.get_category(
        session=session,
        category_id=category_id,
    )


@category_router.get("/", response_model=Page[CategoryRead])
async def get_categories(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    params: Annotated[Params, Depends(Params)],
    user: Annotated[User, Depends(current_active_user)],
):
    stmt = category_service.get_categories_smtp()
    return await paginate(session, stmt, params)
