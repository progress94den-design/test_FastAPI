import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from models.users import User

from core.config import settings


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.cookie.reset_password_token_secret
    verification_token_secret = settings.cookie.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Request | None = None,
    ):
        print(f"User {user.id} has registered.")

    # async def on_after_forgot_password(
    #     self, user: User, token: str, request: Request | None = None
    # ):
    #     print(f"User {user.id} has forgot their password. Reset token: {token}")
    #
    # async def on_after_request_verify(
    #     self, user: User, token: str, request: Request | None = None
    # ):
    #     print(f"Verification requested for user {user.id}. Verification token: {token}")
