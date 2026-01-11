from sqlalchemy.ext.asyncio import AsyncSession

from crud.article import CRUDArticle
from schemas.article import ArticleCreate
from models.users import User
from models.article import Article


class ArticleService:

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
