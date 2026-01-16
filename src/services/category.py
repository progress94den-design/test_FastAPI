from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy.sql import Select

from crud.category import CRUDCategory
from schemas.category import CategoryCreate
from models.category import Category


class CategoryService:

    def __init__(self, crud: CRUDCategory) -> None:
        self.crud = crud

    async def get_category(
        self,
        session: AsyncSession,
        category_id: UUID,
    ) -> Category:

        category = await self.crud.get_by_id(
            obj_id=category_id,
            session=session,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id:{category_id} not found",
            )

        return category

    def get_categories_smtp(self) -> Select:
        return self.crud.get_list_stmt()

    async def create_category(
        self,
        data: CategoryCreate,
        session: AsyncSession,
    ) -> Category:
        try:
            category = await self.crud.create(
                data={"name": data.name},
                session=session,
            )
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name {data.name} already exists",
            )

        await session.refresh(category)
        return category


category_service: CategoryService = CategoryService(CRUDCategory())
