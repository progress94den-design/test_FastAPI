from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(
        self,
        data: dict,
        session: AsyncSession,
    ) -> ModelType:
        obj = self.model(**data)
        session.add(obj)
        await session.flush()  # получаем id, не коммитя
        return obj
