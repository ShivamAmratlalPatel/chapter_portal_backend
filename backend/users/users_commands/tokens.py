"""Module contains the function to create an access token for a user."""
from datetime import timedelta
from uuid import UUID

from jose import jwt

from backend.config import ALGORITHM, SECRET_KEY
from backend.utils import datetime_now


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
    chapter_id: UUID | None = None,
) -> str:
    """Create access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime_now() + expires_delta
    else:
        expire = datetime_now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    if chapter_id:
        to_encode.update({"chapter_id": str(chapter_id)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
