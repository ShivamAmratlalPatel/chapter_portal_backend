"""Allocation Schemas"""

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.chapters.chapters_schemas import ChapterRead
from backend.utils import datetime_now, generate_uuid


class AllocationBase(BaseModel):
    """Allocation Base"""

    section_id: int
    chapter_id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "section_id": 1,
            "chapter_id": generate_uuid(),
        },
    )


class AllocationCreate(AllocationBase):
    """Allocation Create"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **AllocationBase.model_config["json_schema_extra"],
        },
    )


class AllocationRead(AllocationBase):
    """Allocation Read"""

    id: UUID
    user_name: str
    section_name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **AllocationBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
            "user_name": "User Name",
            "section_name": "Section Name",
        },
    )
