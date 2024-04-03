"""Committee Database Models"""
from sqlalchemy import Boolean, Column, DateTime, String, func, ForeignKey, Date
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class CommitteeMember(Base):
    """Committee Member database model."""

    __tablename__ = "committee_members"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=False)
    chapter_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("chapters.id"),
        nullable=False,
    )
    position = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    commencement_date = Column(Date, nullable=False)
    conclusion_date = Column(Date, nullable=True)
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

    chapter = relationship("Chapter")

    @property
    def is_current(self: "CommitteeMember") -> bool:
        """
        Check if the committee member is current.

        Returns:
            bool: True if the committee member is current, False otherwise.

        """
        return self.conclusion_date is None

    @property
    def is_past(self: "CommitteeMember") -> bool:
        """
        Check if the committee member is past.

        Returns:
            bool: True if the committee member is past, False otherwise.

        """
        return not self.is_current

    @property
    def is_upcoming(self: "CommitteeMember") -> bool:
        """
        Check if the committee member is upcoming.

        Returns:
            bool: True if the committee member is upcoming, False otherwise.

        """
        return self.commencement_date > datetime_now().date()
