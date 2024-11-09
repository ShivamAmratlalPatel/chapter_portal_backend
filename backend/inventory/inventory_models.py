"""Inventory Database Models"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.utils import datetime_now, generate_uuid


class Category(Base):
    """Category Database Model"""

    __tablename__ = "category"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")


class Location(Base):
    """Location Database Model"""

    __tablename__ = "location"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")


class InventoryItem(Base):
    """Inventory Item Database Model"""

    __tablename__ = "inventory_item"

    id = Column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=generate_uuid(),
        server_default=func.uuid_generate_v4(),
    )
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    category_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("category.id"),
        nullable=True,
    )
    location_id = Column(
        pg.UUID(as_uuid=True),
        ForeignKey("location.id"),
        nullable=True,
    )
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")
    created_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime_now(),
        server_default=func.timezone("Europe/London", func.current_timestamp()),
    )
    last_modified_date = Column(
        DateTime(timezone=True),
        onupdate=datetime_now(),
        server_onupdate=func.timezone("Europe/London", func.current_timestamp()),
    )

    category = relationship("Category")
    location = relationship("Location")
