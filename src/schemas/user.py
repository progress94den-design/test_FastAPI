import uuid

from fastapi_users import schemas
from pydantic_extra_types.phone_numbers import PhoneNumber


class BaseUser:
    phone: PhoneNumber


class UserRead(schemas.BaseUser[uuid.UUID], BaseUser):
    pass


class UserCreate(schemas.BaseUserCreate, BaseUser):
    pass


class UserUpdate(schemas.BaseUserUpdate, BaseUser):
    pass
