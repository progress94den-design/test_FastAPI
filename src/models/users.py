from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    phone_number: Mapped[str]

    @classmethod
    def get_db(cls, session: AsyncSession) -> SQLAlchemyUserDatabase:
        return SQLAlchemyUserDatabase(session, User)
