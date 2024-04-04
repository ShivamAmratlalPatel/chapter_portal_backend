"""Save a testing chapter."""
from sqlalchemy.orm import Session

from backend.chapters.chapters_models import Chapter
from testing.helpers.fake_data import fake_email, fake_name, fake_zone


def save_testing_chapter(
    session: Session,
    name: str | None = None,
    zone: str | None = None,
) -> Chapter:
    """
    Save a testing chapter.

    Args:
        session (Session): Database session
        name (str, optional): Chapter name. Defaults to None in which case a fake name is generated.
        zone (str, optional): Chapter zone. Defaults to None in which case a fake zone is generated.

    Returns:
        Chapter: A chapter instance.

    """
    chapter = Chapter(
        name=name if name else fake_name(),
        zone=zone if zone else fake_zone(),
        email=fake_email(),
    )

    session.add(chapter)
    session.commit()

    return chapter
