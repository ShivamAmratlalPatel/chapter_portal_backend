"""Update Schemas"""
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.chapters.chapters_schemas import ChapterRead
from backend.utils import datetime_now, generate_uuid


class EventTypeBase(BaseModel):
    """Base Event Type Schema"""

    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "name": "Event Type Name",
            "created_date": datetime_now().date(),
        },
    )

class EventTypeRead(EventTypeBase):
    """Read Event Type Schema"""

    id: UUID
    created_date: datetime


    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **EventTypeBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
        },
    )

class EventSubTypeBase(BaseModel):
    """Base Event SUb Type Schema"""

    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "name": "Event Sub Type Name",
            "created_date": datetime_now().date(),
        },
    )

class EventSubTypeRead(EventSubTypeBase):
    """Read Event Sub Type Schema"""

    id: UUID
    created_date: datetime


    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **EventSubTypeBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
        },
    )



class EventBase(BaseModel):
    """Base Event Schema"""

    name: str
    event_date: date
    event_type_id: UUID
    event_sub_type_id: UUID | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "name": "Event Name",
            "event_type_id": generate_uuid(),
        },
    )


class EventCreate(EventBase):
    """Create Event Schema"""

    chapter_ids: list[UUID] | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **EventBase.model_config["json_schema_extra"],
        },
    )

class EventUpdate(EventBase):
    """Update Event Schema"""


    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **EventCreate.model_config["json_schema_extra"],
        },
    )


class EventRead(EventBase):
    """Read Event Schema"""

    id: UUID
    chapters: list[ChapterRead] | None = None
    created_date: datetime
    event_type: EventTypeRead
    event_sub_type: EventSubTypeRead | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **EventBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
            "chapters": [],
        },
    )

