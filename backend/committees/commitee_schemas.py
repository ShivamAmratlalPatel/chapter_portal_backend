"""Update Schemas"""
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from backend.utils import datetime_now, generate_uuid
from testing.helpers.fake_data import fake_email


class CommitteeBase(BaseModel):
    """Base Committee Schema"""

    name: str
    chapter_id: UUID
    position: str
    email: str | None = None
    phone: str | None = None
    commencement_date: date
    conclusion_date: date | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "name": "Committee Name",
            "chapter_id": generate_uuid(),
            "position": "Committee Position",
            "email": fake_email(),
            "phone": "+447123456789",
            "commencement_date": datetime_now().date(),
            "conclusion_date": None,
        },
    )


class CommitteeCreate(CommitteeBase):
    """Create Committee Schema"""

    natcom_buddy_name: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **CommitteeBase.model_config["json_schema_extra"],
        },
    )


class CommitteeRead(CommitteeBase):
    """Read Committee Schema"""

    id: UUID
    natcom_buddy_name: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **CommitteeBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
            "natcom_buddy_name": "Chapter Buddy Name",
        },
    )
