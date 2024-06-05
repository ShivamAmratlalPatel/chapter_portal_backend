"""Actions Schemas"""

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.utils import generate_uuid, datetime_now


class ActionBase(BaseModel):
    """Action Base"""

    section_id: int | None = None
    chapter_id: UUID | None = None
    note: str
    due_date: date | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "user_id": generate_uuid(),
            "section_id": 1,
            "chapter_id": generate_uuid(),
            "note": "Note",
            "due_date": datetime_now().date(),
        },
    )


class ActionCreate(ActionBase):
    """Action Create"""

    assignee_name: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **ActionBase.model_config["json_schema_extra"],
        },
    )


class ActionUpdate(ActionCreate):
    """Action Create"""

    completed_date: date | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **ActionBase.model_config["json_schema_extra"],
        },
    )


class ActionRead(ActionBase):
    """Action Read"""

    id: UUID
    assignee_name: str | None = None
    chapter_name: str | None = None
    section_name: str | None = None
    created_user_name: str
    completed_date: date | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **ActionBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
            "assignee_name": "Assignee Name",
            "chapter_name": "Chapter Name",
            "section_name": "Section Name",
            "created_user_name": "Created User Name",
            "completed_date": datetime_now().date(),
        },
    )


class Assignee(BaseModel):
    full_name: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "full_name": "Full Name",
        },
    )
