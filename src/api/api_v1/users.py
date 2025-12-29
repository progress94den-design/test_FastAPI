from fastapi import APIRouter

from api.dependencies.authentication.fastapi_users_routers import fastapi_users
from schemas.user import UserRead, UserUpdate

users_router = APIRouter()

# /me
# /{id}
users_router.include_router(
    router=fastapi_users.get_users_router(UserRead, UserUpdate),
)


@users_router.delete("/{id}")
def delete_user(id: str) -> dict[str, str]:
    return {
        "message": "Метод не доступен",
    }
