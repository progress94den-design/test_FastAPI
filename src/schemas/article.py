from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


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

    model_config = ConfigDict(from_attributes=True)


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)


class ArticleCategoriesUpdate(BaseModel):
    category_ids: Optional[list[UUID]] = Field(default=None)
