from pydantic import BaseModel, ConfigDict
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

    image: str

    model_config = ConfigDict(from_attributes=True)
