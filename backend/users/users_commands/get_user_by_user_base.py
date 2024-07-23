from fastapi import HTTPException
from starlette import status

from backend.users.users_models import User


def get_user_by_user_base(current_user, db) -> User:
    """Get a user by user base."""
    user: User | None = (
        db.query(User)
        .filter_by(email=current_user.email)
        .filter_by(is_deleted=False)
        .filter_by(full_name=current_user.full_name)
        .order_by(User.created_date.desc())
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
