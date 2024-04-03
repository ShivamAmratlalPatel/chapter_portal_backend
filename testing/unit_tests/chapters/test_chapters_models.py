"""Test cases for chapters models."""
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.chapters.chapters_models import Chapter
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import fake_chapter


class TestChapter:
    """Chapter model test cases."""

    def test_create_chapter(self: "TestChapter", session: Session) -> None:
        """Test creating a chapter instance."""
        chapter_data = fake_chapter()
        chapter = Chapter(**chapter_data)
        session.add(chapter)
        session.commit()

        assert chapter.id is not None
        assert chapter.name == chapter_data["name"]
        assert chapter.zone == chapter_data["zone"]
        assert chapter.email == chapter_data["email"]
        assert chapter.created_date is not None
        assert chapter.is_deleted is False

    def test_unique_email_constraint(self: "TestChapter", session: Session) -> None:
        """Test uniqueness constraint for email."""
        chapter_data = fake_chapter()

        chapter1 = Chapter(**chapter_data)
        chapter2 = Chapter(**chapter_data)

        session.add(chapter1)
        session.commit()
        session.add(chapter2)
        with pytest.raises(IntegrityError):
            session.commit()

    def test_soft_delete_chapter(self: "TestChapter", session: Session) -> None:
        """Test soft deleting a chapter."""
        chapter_data = fake_chapter()

        chapter = Chapter(**chapter_data)
        session.add(chapter)
        session.commit()

        chapter.is_deleted = True
        session.commit()

        deleted_chapter = session.get(Chapter, chapter.id)
        assert deleted_chapter.is_deleted is True
