"""Endpoints for meetings"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.meetings.meetings_models import (
    MatrixMeeting,
    ZonalTeamMeeting,
    SectionMeeting,
)
from backend.meetings.meetings_schemas import (
    MatrixMeetingCreate,
    MatrixMeetingUpdate,
    MatrixMeetingRead,
    ZonalTeamMeetingCreate,
    ZonalTeamMeetingUpdate,
    ZonalTeamMeetingRead,
    SectionMeetingCreate,
    SectionMeetingUpdate,
    SectionMeetingRead,
)

from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_user_by_user_base import get_user_by_user_base
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_models import User, UserType
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict, generate_uuid

meetings_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@meetings_router.post(
    "/matrix_meeting",
    response_model=MatrixMeetingRead,
    tags=["meetings"],
)
def create_matrix_meeting(
    meeting: MatrixMeetingCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a matrix meeting."""
    check_admin(current_user)

    meeting = MatrixMeeting(
        id=generate_uuid(),
        zone=meeting.zone,
        meeting_date=meeting.meeting_date,
        agenda=meeting.agenda,
        minutes_link=meeting.minutes_link,
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(MatrixMeetingRead.model_validate(meeting)),
    )


@meetings_router.put(
    "/matrix_meeting/{meeting_id}",
    response_model=MatrixMeetingRead,
    tags=["meetings"],
)
def update_matrix_meeting(
    meeting_id: UUID,
    meeting: MatrixMeetingUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a matrix meeting."""
    check_admin(current_user)

    meeting_instance: MatrixMeeting | None = db.get(MatrixMeeting, meeting_id)

    if meeting_instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    meeting_instance.zone = meeting.zone
    meeting_instance.meeting_date = meeting.meeting_date
    meeting_instance.agenda = meeting.agenda
    meeting_instance.minutes_link = meeting.minutes_link

    db.commit()
    db.refresh(meeting_instance)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(MatrixMeetingRead.model_validate(meeting_instance)),
    )


@meetings_router.get(
    "/matrix_meeting/{meeting_id}",
    response_model=MatrixMeetingRead,
    tags=["meetings"],
)
def read_matrix_meeting(
    meeting_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read a matrix meeting."""
    check_admin(current_user)

    meeting: MatrixMeeting | None = db.get(MatrixMeeting, meeting_id)

    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(MatrixMeetingRead.model_validate(meeting)),
    )


@meetings_router.delete(
    "/matrix_meeting/{meeting_id}",
    tags=["meetings"],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_matrix_meeting(
    meeting_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Delete a matrix meeting."""
    check_admin(current_user)

    meeting: MatrixMeeting | None = db.get(MatrixMeeting, meeting_id)

    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    meeting.is_deleted = True
    db.commit()

    return


@meetings_router.post(
    "/zonal_team_meeting",
    response_model=ZonalTeamMeetingRead,
    tags=["meetings"],
)
def create_zonal_team_meeting(
    meeting: ZonalTeamMeetingCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a zonal team meeting."""
    check_admin(current_user)

    meeting = ZonalTeamMeeting(
        id=generate_uuid(),
        zone=meeting.zone,
        meeting_date=meeting.meeting_date,
        agenda=meeting.agenda,
        minutes_link=meeting.minutes_link,
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(ZonalTeamMeetingRead.model_validate(meeting)),
    )


@meetings_router.put(
    "/zonal_team_meeting/{meeting_id}",
    response_model=ZonalTeamMeetingRead,
    tags=["meetings"],
)
def update_zonal_team_meeting(
    meeting_id: UUID,
    meeting: ZonalTeamMeetingUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a zonal team meeting."""
    check_admin(current_user)

    meeting_instance: ZonalTeamMeeting | None = db.get(ZonalTeamMeeting, meeting_id)

    if meeting_instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    meeting_instance.zone = meeting.zone
    meeting_instance.meeting_date = meeting.meeting_date
    meeting_instance.agenda = meeting.agenda
    meeting_instance.minutes_link = meeting.minutes_link

    db.commit()
    db.refresh(meeting_instance)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(ZonalTeamMeetingRead.model_validate(meeting_instance)),
    )


@meetings_router.get(
    "/zonal_team_meeting/{meeting_id}",
    response_model=ZonalTeamMeetingRead,
    tags=["meetings"],
)
def read_zonal_team_meeting(
    meeting_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read a zonal team meeting."""
    check_admin(current_user)

    meeting: ZonalTeamMeeting | None = db.get(ZonalTeamMeeting, meeting_id)

    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(ZonalTeamMeetingRead.model_validate(meeting)),
    )


@meetings_router.delete(
    "/zonal_team_meeting/{meeting_id}",
    tags=["meetings"],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_zonal_team_meeting(
    meeting_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Delete a zonal team meeting."""
    check_admin(current_user)

    meeting: ZonalTeamMeeting | None = db.get(ZonalTeamMeeting, meeting_id)

    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    meeting.is_deleted = True
    db.commit()

    return


@meetings_router.post(
    "/section_meeting",
    response_model=SectionMeetingRead,
    tags=["meetings"],
)
def create_section_meeting(
    meeting: SectionMeetingCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a section meeting."""
    check_admin(current_user)

    meeting = SectionMeeting(
        id=generate_uuid(),
        section_id=meeting.section_id,
        meeting_date=meeting.meeting_date,
        agenda=meeting.agenda,
        minutes_link=meeting.minutes_link,
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(SectionMeetingRead.model_validate(meeting)),
    )


@meetings_router.put(
    "/section_meeting/{meeting_id}",
    response_model=SectionMeetingRead,
    tags=["meetings"],
)
def update_section_meeting(
    meeting_id: UUID,
    meeting: SectionMeetingUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a section meeting."""
    check_admin(current_user)

    meeting_instance: SectionMeeting | None = db.get(SectionMeeting, meeting_id)

    if meeting_instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    meeting_instance.section_id = meeting.section_id
    meeting_instance.meeting_date = meeting.meeting_date
    meeting_instance.agenda = meeting.agenda
    meeting_instance.minutes_link = meeting.minutes_link

    db.commit()
    db.refresh(meeting_instance)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(SectionMeetingRead.model_validate(meeting_instance)),
    )


@meetings_router.get(
    "/section_meeting/{meeting_id}",
    response_model=SectionMeetingRead,
    tags=["meetings"],
)
def read_section_meeting(
    meeting_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read a section meeting."""
    check_admin(current_user)

    meeting: SectionMeeting | None = db.get(SectionMeeting, meeting_id)

    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(SectionMeetingRead.model_validate(meeting)),
    )


@meetings_router.delete(
    "/section_meeting/{meeting_id}",
    tags=["meetings"],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_section_meeting(
    meeting_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Delete a section meeting."""
    check_admin(current_user)

    meeting: SectionMeeting | None = db.get(SectionMeeting, meeting_id)

    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    meeting.is_deleted = True
    db.commit()

    return


@meetings_router.get(
    "/matrix_meeting/zone/{zone}",
    response_model=list[MatrixMeetingRead],
    tags=["meetings"],
)
def read_matrix_meetings_by_zone(
    zone: str,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read matrix meetings by zone."""
    check_admin(current_user)

    meetings: list[MatrixMeeting] = (
        db.query(MatrixMeeting)
        .filter_by(zone=zone)
        .filter(MatrixMeeting.is_deleted.is_(False))
        .all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(MatrixMeetingRead.model_validate(meeting))
            for meeting in meetings
        ],
    )


@meetings_router.get(
    "/zonal_team_meeting/zone/{zone}",
    response_model=list[ZonalTeamMeetingRead],
    tags=["meetings"],
)
def read_zonal_team_meetings_by_zone(
    zone: str,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read zonal team meetings by zone."""
    check_admin(current_user)

    meetings: list[ZonalTeamMeeting] = (
        db.query(ZonalTeamMeeting)
        .filter_by(zone=zone)
        .filter(ZonalTeamMeeting.is_deleted.is_(False))
        .all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(ZonalTeamMeetingRead.model_validate(meeting))
            for meeting in meetings
        ],
    )


@meetings_router.get(
    "/section_meeting/section/{section_id}",
    response_model=list[SectionMeetingRead],
    tags=["meetings"],
)
def read_section_meetings_by_section(
    section_id: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read section meetings by section."""
    check_admin(current_user)

    meetings: list[SectionMeeting] = (
        db.query(SectionMeeting)
        .filter_by(section_id=section_id)
        .filter(SectionMeeting.is_deleted.is_(False))
        .all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(SectionMeetingRead.model_validate(meeting))
            for meeting in meetings
        ],
    )
