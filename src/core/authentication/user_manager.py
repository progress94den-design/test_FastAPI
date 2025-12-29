import uuid

from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi import HTTPException
from sqlalchemy import select

from models.users import User
from core.config import settings
from schemas.user import UserCreate


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.cookie.reset_password_token_secret
    verification_token_secret = settings.cookie.verification_token_secret

    async def get_by_phone(self, phone: str) -> User | None:
        stmt = select(User).where(User.phone_number == phone)
        result = await self.user_db.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Request | None = None,
    ):
        user = await self.get_by_phone(user_create.phone_number)
        if user:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким номером телефона уже существует",
            )

        return await super().create(user_create, safe, request)

    async def on_after_register(
        self,
        user: User,
        request: Request | None = None,
    ) -> None:
        print(f"User {user.id} has registered.")
