"""Membership Schemas"""
from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.utils import datetime_now, generate_uuid


class MembershipLogCreate(BaseModel):
    """Membership Log Create Schema"""

    chapter_id: UUID
    number_of_members: int
    log_date: date

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "chapter_id": generate_uuid(),
                "number_of_members": 10,
                "log_date": datetime_now().date(),
            },
        },
    )


class MembershipLogRead(MembershipLogCreate):
    """Membership Log Read Schema"""

    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **MembershipLogCreate.model_config["json_schema_extra"]["example"],
                "id": generate_uuid(),
            },
        },
    )
