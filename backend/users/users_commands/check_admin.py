"""Check if the user is an admin."""
from fastapi import HTTPException
from starlette import status

from backend.users.users_schemas import UserBase


def check_admin(user: UserBase) -> None:
    """Check if the user is an admin."""
    if user.user_type_name in ("admin", "super_admin"):
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
