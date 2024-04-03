"""Chapter Database Models"""
from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


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
    zone = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
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
    teams = relationship("Team", back_populates="chapter")
