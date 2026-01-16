from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy.sql import Select

from crud.category import CRUDCategory
from schemas.category import CategoryCreate, CategoryRead
from models.users import User
from models.category import Category
from services.minio import MinioService, minio_service


class CategoryService:

    def __init__(self, crud: CRUDCategory) -> None:
        self.crud = crud

    async def create_category(
        self,
        data: CategoryCreate,
        session: AsyncSession,
    ) -> Category:
        existing = await self.crud.get_by_name(
            name=data.name,
            session=session,
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name {data.name} already exists",
            )

        category = await self.crud.create(
            data={
                "name": data.name,
            },
            session=session,
        )

        await session.commit()
        await session.refresh(category)
        return category


category_service: CategoryService = CategoryService(CRUDCategory())
