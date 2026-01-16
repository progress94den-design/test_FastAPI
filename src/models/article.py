from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import String, Text, func, ForeignKey, Index, Computed
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import TSVECTOR
from uuid import UUID

if TYPE_CHECKING:
    from models.users import User
    from models.category import Category

from models.base import Base
from models.mixins.uuid_pk import UUIDPkMixin


class ArticleBase(UUIDPkMixin, Base):
    __abstract__ = True

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user_id: Mapped["UUID"] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


class Article(ArticleBase):
    __tablename__ = "articles"

    user: Mapped["User"] = relationship(back_populates="articles")
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="article_category_associations",
        back_populates="articles",
        lazy="selectin",
    )

    search_vector: Mapped[TSVECTOR] = mapped_column(
        TSVECTOR,
        Computed(
            """to_tsvector(
                'simple',
                coalesce(title, '') || ' ' || coalesce(text, '')
            )""",
            persisted=True,
        ),
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_article_search_vector_gin",
            "search_vector",
            postgresql_using="gin",
        ),
    )


class DeletedArticle(ArticleBase):
    __tablename__ = "deleted_articles"

    deleted_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="deleted_articles")
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="article_category_associations",
        lazy="selectin",
    )
