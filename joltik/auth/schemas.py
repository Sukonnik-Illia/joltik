import uuid
from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    # below are extract from the library:
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    # add fields from our class User:
    username: str
    registered_at: datetime
    role_fk: uuid.UUID


class UserCreate(schemas.BaseUserCreate):
    # below are extract from the library:
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    # add fields from our class User:
    username: str
    role_fk: uuid.UUID
