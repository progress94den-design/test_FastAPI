from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy.sql import Select

from crud.article import CRUDArticle
from schemas.article import ArticleCreate
from models.users import User
from models.article import Article


class ArticleService:

    @staticmethod
    async def get_article(
        session: AsyncSession,
        article_id: UUID,
    ) -> Article:
        repo = CRUDArticle()

        article = await repo.get_by_id(
            obj_id=article_id,
            session=session,
        )

        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with id:{article_id} not found",
            )

        return article

    @staticmethod
    def get_articles_stmt(*, search: str | None = None) -> Select:
        repo = CRUDArticle()

        if search:
            return repo.search_stmt(query=search)

        return repo.get_list_stmt()

    @staticmethod
    async def create_article(
        data: ArticleCreate,
        session: AsyncSession,
        user: User,
    ) -> Article:
        repo = CRUDArticle()

        article = await repo.create(
            data={
                "title": data.title,
                "text": data.text,
                "user_id": user.id,
            },
            session=session,
        )

        await session.commit()
        return article
