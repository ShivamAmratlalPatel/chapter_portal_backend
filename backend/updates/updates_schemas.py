"""Update Schemas"""
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from backend.utils import datetime_now, generate_uuid


class ChapterUpdateBase(BaseModel):
    """Base Chapter Update Schema"""

    chapter_id: UUID
    update_date: date | datetime
    update_text: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "chapter_id": generate_uuid(),
            "update_date": datetime_now().date(),
            "update_text": "Update text here",
        },
    )

    @field_validator("update_date", mode="before")
    @classmethod
    def convert_datetime_to_date(cls, obj: date | datetime) -> date:
        if isinstance(obj, datetime):
            return obj.date()
        return obj


class ChapterUpdateCreate(ChapterUpdateBase):
    """Create Chapter Update Schema"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **ChapterUpdateBase.model_config["json_schema_extra"],
        },
    )


class ChapterUpdateRead(ChapterUpdateBase):
    """Read Chapter Update Schema"""

    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **ChapterUpdateBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
        },
    )


class SectionUpdateBase(BaseModel):
    """Base Section Update Schema"""

    section_id: int
    update_date: date
    update_text: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "section_id": 1,
            "update_date": datetime_now().date(),
            "update_text": "Update text here",
        },
    )


class SectionUpdateCreate(SectionUpdateBase):
    """Create Section Update Schema"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **SectionUpdateBase.model_config["json_schema_extra"],
        },
    )


class SectionUpdateRead(SectionUpdateBase):
    """Read Section Update Schema"""

    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **SectionUpdateBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
        },
    )
