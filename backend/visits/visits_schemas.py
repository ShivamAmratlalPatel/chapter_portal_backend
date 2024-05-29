"""Visits Schemas"""

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.chapters.chapters_schemas import ChapterRead
from backend.utils import datetime_now, generate_uuid


class VisitBase(BaseModel):
    """Visit Base"""

    visit_date: date
    visit_category_id: UUID
    comments: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "visit_date": datetime_now().date(),
            "visit_category_id": generate_uuid(),
            "comments": "Comments here",
        },
    )


class VisitCreate(VisitBase):
    """Visit Create"""

    chapter_ids: list[UUID]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **VisitBase.model_config["json_schema_extra"],
        },
    )


class VisitRead(VisitBase):
    """Visit Read"""

    id: UUID
    visit_category: dict
    chapters: list[ChapterRead]
    user_name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **VisitBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
        },
    )
