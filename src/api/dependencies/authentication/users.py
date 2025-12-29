from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, AsyncGenerator

from core.db_helper import db_helper
from models.users import User


async def get_users_db(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> AsyncGenerator[AsyncSession, None]:
    yield User.get_db(session=session)
