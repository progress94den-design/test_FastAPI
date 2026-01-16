from crud.base import CRUDBase
from models.category import Category
from sqlalchemy import select
from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDCategory(CRUDBase[Category]):
    def __init__(self):
        super().__init__(Category)

    def get_list_stmt(self) -> Select:
        stmt = select(self.model).order_by(self.model.name)
        return stmt

    async def get_by_name(self, session: AsyncSession, name: str) -> Category | None:
        stmt = select(self.model).where(self.model.name == name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
