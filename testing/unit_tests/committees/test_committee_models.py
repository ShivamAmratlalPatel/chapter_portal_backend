"""Test committee member model."""
from datetime import timedelta

from sqlalchemy.orm import Session

from backend.committees.committee_models import CommitteeMember
from backend.utils import datetime_now
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.setup.save_testing_chapter import save_testing_chapter


class TestCommitteeMember:
    """Test cases for committee member model."""

    def test_committee_member_creation(
        self: "TestCommitteeMember",
        session: Session,
    ) -> None:
        """
        Test creating a committee member instance.

        Args:
            session (Session): Database session

        Returns:
            None

        """
        chapter = save_testing_chapter(session)
        # Create a committee member
        member = CommitteeMember(
            name="John Doe",
            chapter_id=chapter.id,
            position="Chairperson",
            commencement_date=datetime_now().date(),
        )
        session.add(member)
        session.commit()

        # Retrieve the committee member
        retrieved_member = (
            session.query(CommitteeMember).filter_by(name="John Doe").first()
        )

        # Check if the retrieved member matches the created member
        assert retrieved_member is not None
        assert retrieved_member.name == "John Doe"
        assert retrieved_member.position == "Chairperson"
        assert retrieved_member.commencement_date == datetime_now().date()

    def test_committee_member_properties(self: "TestCommitteeMember") -> None:
        """
        Test the properties of the committee member model.

        Returns
            None

        """
        # Create a committee member
        member = CommitteeMember(
            name="Jane Doe",
            chapter_id="123e4567-e89b-12d3-a456-426614174000",  # Example UUID
            position="Vice Chairperson",
            commencement_date=datetime_now().date(),
            conclusion_date=None,
        )

        assert member.is_current is True
        assert member.is_past is False
        assert member.is_upcoming is False

        # Set the conclusion date
        member.commencement_date = datetime_now().date() - timedelta(days=2)
        member.conclusion_date = datetime_now().date() - timedelta(days=1)
        assert member.is_current is False
        assert member.is_past is True
        assert member.is_upcoming is False

        # Set the commencement date to tomorrow
        member.commencement_date = datetime_now().date() + timedelta(days=1)
        member.conclusion_date = None
        assert member.is_current is False
        assert member.is_past is False
        assert member.is_upcoming is True
