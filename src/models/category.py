from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from uuid import UUID

if TYPE_CHECKING:
    from models.article import Article, DeletedArticle

from models.base import Base
from models.mixins.uuid_pk import UUIDPkMixin


class Category(UUIDPkMixin, Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    articles: Mapped[list["Article"]] = relationship(
        "Article",
        secondary="article_category_associations",
        back_populates="categories",
        lazy="selectin",
    )
    deleted_articles: Mapped[list["DeletedArticle"]] = relationship(
        "DeletedArticle",
        secondary="deleted_article_category_associations",
        back_populates="categories",
        lazy="selectin",
    )


class ArticleCategoryAssociation(Base):
    __tablename__ = "article_category_associations"

    article_id: Mapped["UUID"] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    category_id: Mapped["UUID"] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )


class DeletedArticleCategoryAssociation(Base):
    __tablename__ = "deleted_article_category_associations"

    deleted_article_id: Mapped["UUID"] = mapped_column(
        ForeignKey("deleted_articles.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    category_id: Mapped["UUID"] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
