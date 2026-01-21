from fastapi_users.authentication import AuthenticationBackend

from core.authentication.transport import cookie_transport
from api.dependencies.authentication.strategy import get_jwt_strategy

authentication_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
