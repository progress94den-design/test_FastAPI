from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field
from uuid import UUID
from datetime import datetime

from schemas.category import CategoryRead


class ArticleBase(BaseModel):
    title: str
    text: str


class ArticleCreate(ArticleBase):
    pass


class ArticleRead(ArticleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    user_id: UUID
    image: str | None
    categories: list[CategoryRead] = Field(exclude=True)

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def category_ids(self) -> list[UUID]:
        return [category.id for category in self.categories]


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)


class ArticleCategoriesUpdate(BaseModel):
    category_ids: Optional[list[UUID]] = Field(default=None)
