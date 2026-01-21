from typing import Annotated
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

from core.authentication.user_manager import UserManager
from api.dependencies.authentication.users import get_users_db


async def get_user_manager(
    users_db: Annotated[
        SQLAlchemyUserDatabase,
        Depends(get_users_db),
    ],
) -> UserManager:
    yield UserManager(users_db)
