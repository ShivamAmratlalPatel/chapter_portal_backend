"""Visits Models"""
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class VisitCategory(Base):
    """Visit Categories"""

    __tablename__ = "visit_categories"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    created_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime_now(),
        server_default=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )
    is_deleted = Column(Boolean, nullable=False, default=False)
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )

    name = Column(String, nullable=False)


class Visit(Base):
    """Vists Table"""

    __tablename__ = "visits"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )

    created_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime_now(),
        server_default=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )
    is_deleted = Column(Boolean, nullable=False, default=False)
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )

    visit_date = Column(Date, nullable=False)
    user_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    visit_category_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("visit_categories.id"),
        nullable=False,
    )
    comments = Column(String, nullable=True)

    visit_category = relationship("VisitCategory")
    user = relationship("User")

    chapter_visit_association = relationship(
        "ChapterVisitAssociation",
        back_populates="visit",
    )

    @property
    def chapters(self: "Visit") -> list:
        """Get a list of chapters associated with the visit."""
        chapters = [
            association.chapter
            for association in self.chapter_visit_association
            if not association.is_deleted and not association.chapter.is_deleted
        ]

        return sorted(chapters, key=lambda x: x.name)

    @property
    def user_name(self: "Visit") -> str:
        """Get the user's name."""
        return self.user.full_name


class ChapterVisitAssociation(Base):
    """Chapter Visit Association table."""

    __tablename__ = "chapter_visit_association"
    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid,
        server_default=func.uuid_generate_v4(),
    )
    visit_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("visits.id", ondelete="CASCADE"),
        nullable=False,
    )
    chapter_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_deleted = Column(Boolean, nullable=False, default=False)
    visit = relationship("Visit")
    chapter = relationship("Chapter")
