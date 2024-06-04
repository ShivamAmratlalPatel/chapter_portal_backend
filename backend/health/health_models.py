"""Health Database Models"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class Section(Base):
    """Section Database Model"""

    __tablename__ = "section"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")
    icon = Column(String, nullable=True)


class HealthQuestion(Base):
    """Health Question Database Model"""

    __tablename__ = "health_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    section_id = Column(
        Integer,
        ForeignKey("section.id"),
        nullable=False,
    )
    rag_guide = Column(String, nullable=True)
    created_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime_now(),
        server_default=func.timezone("Europe/London", func.current_timestamp()),
    )
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone("Europe/London", func.current_timestamp()),
    )

    section = relationship("Section")


class ChapterHealth(Base):
    """Chapter Health Database Model"""

    __tablename__ = "chapter_health"

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
    health_question_id = Column(
        Integer,
        ForeignKey("health_questions.id"),
        nullable=False,
    )
    score = Column(Integer, nullable=True)
    comments = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)

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

    health_question = relationship("HealthQuestion")
