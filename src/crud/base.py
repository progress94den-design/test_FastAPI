from typing import Generic, Type, TypeVar, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(
        self,
        obj_id: Any,
        session: AsyncSession,
    ) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        data: dict,
        session: AsyncSession,
    ) -> ModelType:
        obj = self.model(**data)
        session.add(obj)
        await session.flush()  # получаем id, не коммитя
        return obj
