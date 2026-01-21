from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from models.article import Article, DeletedArticle


from models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    phone_number: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

    articles: Mapped[list["Article"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    deleted_articles: Mapped[list["DeletedArticle"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @classmethod
    def get_db(cls, session: AsyncSession) -> SQLAlchemyUserDatabase:
        return SQLAlchemyUserDatabase(session, User)
