"""Chapter Database Models"""
from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid
from backend.visits.visits_models import Visit


class Chapter(Base):
    """Chapter database model."""

    __tablename__ = "chapters"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=False)
    zone = Column(String)
    email = Column(String, nullable=True)
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

    chapter_visit_association = relationship(
        "ChapterVisitAssociation",
        back_populates="chapter",
    )

    @property
    def to(self: "Chapter") -> str:
        """Return the chapter's URL path."""
        return f"/chapter/{self.id}"

    @property
    def visits(self: "Chapter") -> list[Visit]:
        """Get a list of visits associated with the chapter."""
        visits: list[Visit] = [
            association.visit
            for association in self.chapter_visit_association
            if not association.is_deleted and not association.visit.is_deleted
        ]

        # Sort visits by visit date descending
        return sorted(visits, key=lambda visit: visit.visit_date, reverse=True)
