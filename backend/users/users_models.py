"""Users Database Models"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class UserType(Base):
    """UserType database model."""

    __tablename__ = "user_types"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=False)


class User(Base):
    """Users database model."""

    __tablename__ = "users"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
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
    chapter_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=True,
    )
    user_type_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("user_types.id", ondelete="CASCADE"),
        nullable=False,
    )
    chapter = relationship("Chapter")
    user_type = relationship("UserType")

    @property
    def user_type_name(self: "User") -> str:
        """Get user type name."""
        return self.user_type.name
