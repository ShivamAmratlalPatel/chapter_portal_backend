"""Action Database Models"""
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Date,
    Integer,
    func,
    ForeignKey,
    String,
)
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class Action(Base):
    """Action database model"""

    __tablename__ = "actions"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    assignee_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    section_id = Column(
        Integer,
        ForeignKey("section.id"),
        nullable=True,
    )
    chapter_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("chapters.id"),
        nullable=True,
    )
    note = Column(String, nullable=False, default="", server_default="")
    due_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)

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

    created_user_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    assignee = relationship("User", foreign_keys=[assignee_id])
    created_user = relationship("User", foreign_keys=[created_user_id])
    section = relationship("Section")
    chapter = relationship("Chapter")

    @property
    def assignee_name(self: "Action") -> str | None:
        """Get the assignee's name."""
        if self.assignee:
            return self.assignee.full_name
        return None

    @property
    def created_user_name(self: "Action") -> str:
        """Get the created user's name."""
        return self.created_user.full_name

    @property
    def section_name(self: "Action") -> str | None:
        """Get the section's name."""
        if self.section:
            return self.section.name
        return None

    @property
    def chapter_name(self: "Action") -> str | None:
        """Get the chapter's name."""
        if self.chapter:
            return self.chapter.name
        return None
