"""User schemas"""
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """User base."""

    username: str
    email: str | None = None
    full_name: str | None = None
    is_deleted: bool | None = None
    user_type_name: str | None = None
    chapter_id: UUID | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class Token(BaseModel):
    """Token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data."""

    username: str | None = None


class UserCreate(BaseModel):
    """User create."""

    username: str
    email: EmailStr
    password: str
    full_name: str


class UserCreateChapter(UserCreate):
    """User create chapter."""

    chapter_id: UUID
