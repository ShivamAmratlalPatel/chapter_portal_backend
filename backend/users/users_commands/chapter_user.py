"""Verify that the user is part of the chapter."""
from uuid import UUID


def verify_chapter_user(user_chapter_id: UUID, chapter_id: UUID) -> None:
    """Verify that the user is part of the chapter."""
    if user_chapter_id == chapter_id:
        return
    else:
        msg = "User not part of chapter"
        raise ValueError(msg)
