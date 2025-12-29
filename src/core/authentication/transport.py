from fastapi_users.authentication import CookieTransport

from core.config import settings

cookie_transport = CookieTransport(
    cookie_max_age=settings.cookie.cookie_max_age,
)
