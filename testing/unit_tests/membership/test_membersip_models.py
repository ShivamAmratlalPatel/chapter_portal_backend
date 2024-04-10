"""Test membership mod3els"""
from sqlalchemy.orm import Session

from backend.membership.membership_models import MembershipLog
from backend.utils import datetime_now
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.setup.save_testing_chapter import save_testing_chapter


def test_membership_log_creation(session: Session) -> None:
    """
    Test creating a membership log.

    Args:
        session (Session): Database session

    Returns:
        None

    """
    chapter = save_testing_chapter(session)
    # Create a membership log
    membership_log = MembershipLog(
        chapter_id=chapter.id,
        number_of_members=100,
        log_date=datetime_now(),
    )
    session.add(membership_log)
    session.commit()

    # Retrieve the membership log
    retrieved_log = session.query(MembershipLog).first()

    # Check if the retrieved log matches the created one
    assert retrieved_log is not None
    assert retrieved_log.chapter_id == chapter.id
    assert retrieved_log.number_of_members == 100  # noqa: PLR2004
