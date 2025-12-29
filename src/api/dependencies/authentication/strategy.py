from fastapi_users.authentication import JWTStrategy

from core.config import settings

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.cookie.secret,
        lifetime_seconds=settings.cookie.lifetime_seconds,
    )
