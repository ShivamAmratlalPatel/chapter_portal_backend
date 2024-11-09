"""Chapters Schemas"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from backend.utils import datetime_now, generate_uuid
from testing.helpers.fake_data import fake_email, fake_name, fake_zone


class ZoneEnum(str, Enum):
    """Zone enum."""

    london = "London"
    south = "South"
    north = "North"
    central = "Central"
    school = "School"

    __slots__ = ()


class ChapterBase(BaseModel):
    """Chapter base schema."""

    name: str
    email: EmailStr | None = None
    zone: ZoneEnum | None = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": fake_name(),
                "email": fake_email(),
                "zone": fake_zone(),
            },
        },
    )


class ChapterCreate(ChapterBase):
    """Chapter create schema."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                **ChapterBase.model_config["json_schema_extra"]["example"],
            },
        },
    )


class ChapterUpdate(BaseModel):
    """Chapter update schema."""

    name: str
    email: EmailStr | None = None
    zone: ZoneEnum | None = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": fake_name(),
                "email": fake_email(),
                "zone": fake_zone(),
            },
        },
    )


class ChapterRead(ChapterBase):
    """Chapter read schema."""

    id: UUID
    zone: str | None = None
    created_date: datetime
    last_modified_date: datetime | None = None
    is_deleted: bool
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **ChapterBase.model_config["json_schema_extra"]["example"],
                "id": generate_uuid(),
                "created_date": datetime_now(),
                "last_modified_date": datetime_now(),
                "is_deleted": False,
            },
        },
    )


class ChapterSidebar(BaseModel):
    """Chapter sidebar schema."""

    label: str
    icon: str = "pi pi-fw pi-id-card"
    to: str

    model_config = ConfigDict(
        from_attributes=True,
    )
