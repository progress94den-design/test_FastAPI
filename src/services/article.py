from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy.sql import Select

from crud.article import CRUDArticle
from schemas.article import ArticleCreate, ArticleUpdate
from models.users import User
from models.article import Article, DeletedArticle
from services.minio import MinioService, minio_service


class ArticleService:

    def __init__(self, crud: CRUDArticle, minio: MinioService) -> None:
        self.crud = crud
        self.minio = minio

    async def get_article(
        self,
        session: AsyncSession,
        article_id: UUID,
    ) -> Article:

        article = await self.crud.get_by_id(
            obj_id=article_id,
            session=session,
        )

        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with id:{article_id} not found",
            )

        return article

    def get_articles_stmt(self, search: str | None = None) -> Select:
        if search:
            return self.crud.search_stmt(query=search)

        return self.crud.get_list_stmt()

    async def create_article(
        self,
        data: ArticleCreate,
        session: AsyncSession,
        user: User,
        image: UploadFile | None,
    ) -> Article:
        article = await self.crud.create(
            data={
                "title": data.title,
                "text": data.text,
                "user_id": user.id,
                "image": None,
            },
            session=session,
        )

        if image:
            image_url = await self.minio.upload_file(
                bucket_name="articles",
                file=image,
                user_id=user.id,
                obj_id=article.id,
            )
            article.image = image_url

        await session.commit()
        await session.refresh(article)
        return article

    async def update_article(
        self,
        article_id: UUID,
        data: ArticleUpdate,
        session: AsyncSession,
        user: User,
        image: UploadFile | None,
    ) -> Article:
        article = await self.get_article(article_id=article_id, session=session)

        if user.id != article.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You are not allowed to update this article",
            )

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(article, field, value)

        if image:
            image_url = await self.minio.upload_file(
                bucket_name="articles",
                file=image,
                user_id=user.id,
                obj_id=article.id,
            )
            article.image = image_url

        await session.commit()
        await session.refresh(article)
        return article

    async def delete_article(
        self,
        article_id: UUID,
        session: AsyncSession,
        user: User,
    ) -> None:
        article = await self.get_article(article_id=article_id, session=session)

        if user.id != article.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You are not allowed to deleted this article",
            )

        data = self.crud.copy_model(
            instance=article,
            exclude={
                "search_vector",
            },
        )

        deleted_article = DeletedArticle(**data)

        session.add(deleted_article)
        await session.delete(article)
        await session.commit()


article_service: ArticleService = ArticleService(CRUDArticle(), minio_service)
