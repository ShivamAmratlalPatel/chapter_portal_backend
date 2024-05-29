"""Update Models"""
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class ChapterUpdate(Base):
    """Chapter Updates"""

    __tablename__ = "chapter_updates"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
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
    is_deleted = Column(Boolean, nullable=False, default=False)
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone(
            "Europe/London",
            func.timezone("Europe/London", func.current_timestamp()),
        ),
    )
    update_date = Column(Date, nullable=False)
    update_text = Column(String, nullable=False)

    chapter = relationship("Chapter")


class SectionUpdate(Base):
    """Chapter Updates"""

    __tablename__ = "section_updates"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    section_id = Column(
        Integer,
        ForeignKey("section.id"),
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
    update_date = Column(Date, nullable=False)
    update_text = Column(String)

    section = relationship("Section")
