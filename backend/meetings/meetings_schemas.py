"""Meetings Schemas"""

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.utils import generate_uuid, datetime_now


class MeetingBase(BaseModel):
    """Meeting Base"""

    meeting_date: date
    agenda: str | None = None
    minutes_link: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "meeting_date": datetime_now().date(),
            "agenda": "Agenda",
            "minutes_link": "Minutes Link",
        },
    )


class MatrixMeetingBase(MeetingBase):
    """Matrix Meeting Base"""

    zone: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **MeetingBase.model_config["json_schema_extra"],
            "zone": "Zone",
        },
    )


class MatrixMeetingCreate(MatrixMeetingBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **MatrixMeetingBase.model_config["json_schema_extra"],
        },
    )


class MatrixMeetingUpdate(MatrixMeetingBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **MatrixMeetingBase.model_config["json_schema_extra"],
        },
    )


class MatrixMeetingRead(MatrixMeetingBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **MatrixMeetingBase.model_config["json_schema_extra"],
        },
    )


class ZonalTeamMeetingBase(MeetingBase):
    """Zonal Meeting Base"""

    zone: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **MeetingBase.model_config["json_schema_extra"],
            "zone": "Zone",
        },
    )


class ZonalTeamMeetingCreate(ZonalTeamMeetingBase):
    """Zonal Meeting Create"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **ZonalTeamMeetingBase.model_config["json_schema_extra"],
        },
    )


class ZonalTeamMeetingUpdate(ZonalTeamMeetingBase):
    """Zonal Meeting Update"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **ZonalTeamMeetingBase.model_config["json_schema_extra"],
        },
    )


class ZonalTeamMeetingRead(ZonalTeamMeetingBase):
    """Zonal Meeting Read"""

    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **ZonalTeamMeetingBase.model_config["json_schema_extra"],
        },
    )


class SectionMeetingBase(MeetingBase):
    """Section Meeting Base"""

    section_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **MeetingBase.model_config["json_schema_extra"],
            "section_id": 1,
        },
    )


class SectionMeetingCreate(SectionMeetingBase):
    """Section Meeting Create"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **SectionMeetingBase.model_config["json_schema_extra"],
        },
    )


class SectionMeetingUpdate(SectionMeetingBase):
    """Section Meeting Update"""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **SectionMeetingBase.model_config["json_schema_extra"],
        },
    )


class SectionMeetingRead(SectionMeetingBase):
    """Section Meeting Read"""

    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **SectionMeetingBase.model_config["json_schema_extra"],
        },
    )
