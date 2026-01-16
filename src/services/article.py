from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy.sql import Select

from crud.article import CRUDArticle
from crud.category import CRUDCategory
from schemas.article import ArticleCreate, ArticleUpdate
from models.users import User
from models.article import Article, DeletedArticle
from services.minio import MinioService, minio_service


class ArticleService:

    def __init__(
        self,
        article_crud: CRUDArticle,
        category_crud: CRUDCategory,
        minio: MinioService,
    ) -> None:
        self.article_crud = article_crud
        self.category_crud = category_crud
        self.minio = minio

    async def get_article(
        self,
        session: AsyncSession,
        article_id: UUID,
    ) -> Article:

        article = await self.article_crud.get_by_id(
            obj_id=article_id,
            session=session,
        )

        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with id:{article_id} not found",
            )

        return article

    def get_articles_stmt(
        self,
        search: str | None = None,
        category_id: UUID | None = None,
    ) -> Select:
        if search:
            stmt = self.article_crud.search_stmt(query=search)
        else:
            stmt = self.article_crud.get_list_stmt()

        if category_id:
            stmt = self.article_crud.filter_by_category(
                stmt=stmt,
                category_id=category_id,
            )
        return stmt

    async def set_categories(
        self,
        session: AsyncSession,
        article_id: UUID,
        category_ids: list[UUID] | None,
        user: User,
    ) -> Article:
        article = await self.get_article(
            article_id=article_id,
            session=session,
        )

        if article.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You are not allowed to update this article",
            )

        if category_ids is None:
            return article

        if not category_ids:
            article.categories.clear()
            await session.commit()
            await session.refresh(article)
            return article

        categories = await self.category_crud.get_by_ids(
            session=session,
            ids=category_ids,
        )

        if len(categories) != len(set(category_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more categories not found",
            )

        article.categories = categories

        await session.commit()
        await session.refresh(article)
        return article

    async def create_article(
        self,
        data: ArticleCreate,
        session: AsyncSession,
        user: User,
        image: UploadFile | None,
    ) -> Article:
        article = await self.article_crud.create(
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

        data = self.article_crud.copy_model(
            instance=article,
            exclude={
                "search_vector",
            },
        )

        deleted_article = DeletedArticle(**data)

        session.add(deleted_article)
        await session.delete(article)
        await session.commit()


article_service: ArticleService = ArticleService(
    article_crud=CRUDArticle(),
    category_crud=CRUDCategory(),
    minio=minio_service,
)
