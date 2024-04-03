"""Event Database Models"""
from sqlalchemy import Boolean, Column, DateTime, String, func, ForeignKey
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class EventType(Base):
    """Event Type database model."""

    __tablename__ = "event_types"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=False)
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
    events = relationship("Event", back_populates="event_type")


class Event(Base):
    """Event database model."""

    __tablename__ = "events"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=False)
    event_type_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("event_types.id"),
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
    is_deleted = Column(Boolean, nullable=False, default=False)
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )
    event_type = relationship("EventType", back_populates="events")


class ChapterEventAssociation(Base):
    """Chapter Event Association table."""

    __tablename__ = "chapter_event_association"
    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid,
        server_default=func.uuid_generate_v4(),
    )
    chapter_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("chapters.id"),
        nullable=False,
    )
    event_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("events.id"),
        nullable=False,
    )
    is_deleted = Column(Boolean, nullable=False, default=False)
    chapter = relationship("Chapter")
    event = relationship("Event")
