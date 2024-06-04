"""Allocation Database Models"""
from sqlalchemy import Boolean, Column, DateTime, Integer, func, ForeignKey
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class Allocation(Base):
    """Allocation database model"""

    __tablename__ = "allocations"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    user_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    section_id = Column(
        Integer,
        ForeignKey("section.id"),
        nullable=False,
    )
    chapter_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("chapters.id"),
        nullable=False,
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
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )

    user = relationship("User")
    section = relationship("Section")
    chapter = relationship("Chapter")

    @property
    def user_name(self: "Allocation") -> str:
        """Get the user's name."""
        return self.user.full_name

    @property
    def section_name(self: "Allocation") -> str:
        """Get the section's name."""
        return self.section.name
