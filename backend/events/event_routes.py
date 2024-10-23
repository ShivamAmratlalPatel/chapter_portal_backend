"""Endpoints for events"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.helpers import get_db
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_user_by_user_base import get_user_by_user_base
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_models import User
from backend.users.users_schemas import UserBase
from backend.utils import datetime_now, generate_uuid, object_to_dict

from backend.events.event_schemas import EventBase, EventCreate, EventRead, EventUpdate, EventTypeRead, EventSubTypeRead
from backend.events.event_models import Event, EventType, ChapterEventAssociation, EventSubType

event_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@event_router.post(
    "/event",
    response_model=EventRead,
    tags=["events"],
)
def create_event(
    event_details: EventCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create an event."""
    check_admin(current_user)


    event_type = db.get(EventType, event_details.event_type_id)
    if event_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event Type not found",
        )

    event_sub_type = db.get(EventSubType, event_details.event_sub_type_id)
    if event_sub_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event Sub Type not found",
        )

    for chapter_id in event_details.chapter_ids:
        chapter = db.get(Chapter, chapter_id)
        if chapter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found",
            )

    event = Event(
        id=generate_uuid(),
        name=event_details.name,
        event_type_id=event_details.event_type_id,
        event_sub_type_id=event_details.event_sub_type_id,
        event_date=event_details.event_date,
        created_date=datetime_now(),
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    for chapter_id in event_details.chapter_ids:
        chapter_event_association = ChapterEventAssociation(
            id=generate_uuid(),
            chapter_id=chapter_id,
            event_id=event.id,
            is_deleted=False
        )
        db.add(chapter_event_association)
        db.commit()



    return JSONResponse(content=object_to_dict(EventRead.model_validate(event)))



@event_router.get(
    "/event/{event_id}",
    response_model=EventRead,
    tags=["events"],
)
def read_event(
    event_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read an event."""
    check_admin(current_user)

    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    return JSONResponse(content=object_to_dict(EventRead.model_validate(event)))


@event_router.put(
    "/event/{event_id}",
    response_model=EventRead,
    tags=["events"],
)
def update_event(
    event_id: UUID,
    event_details: EventUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update an event."""
    check_admin(current_user)

    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    event.name = event_details.name
    event.event_type_id = event_details.event_type_id
    event.event_date = event_details.event_date
    event.last_modified_date = datetime_now()

    db.add(event)
    db.commit()
    db.refresh(event)

    return JSONResponse(content=object_to_dict(EventRead.model_validate(event)))


@event_router.delete(
    "/event/{event_id}",
    tags=["events"],
)
def delete_event(
    event_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete an event."""
    check_admin(current_user)

    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    event.is_deleted = True
    event.last_modified_date = datetime_now()

    db.add(event)
    db.commit()

    return JSONResponse(content={"detail": "Event deleted"})


@event_router.get(
    "/events/chapter/{chapter_id}",
    response_model=list[EventRead],
    tags=["events"],
)
def read_events_by_chapter(
    chapter_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read events by chapter."""
    check_admin(current_user)

    events = (
        db.query(Event)
        .join(ChapterEventAssociation)
        .filter(ChapterEventAssociation.chapter_id == chapter_id)
        .filter(Event.is_deleted == False)
        .all()
    )

    return JSONResponse(
        content=[
            object_to_dict(EventRead.model_validate(event), format_date=True)
            for event in events
        ],
    )


@event_router.get(
    "/events/year/{year}/month/{month}",
    response_model=list[EventRead],
    tags=["events"],
)
def read_events_by_year_month(
    year: int,
    month: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read events by year and month."""
    check_admin(current_user)

    events = (
        db.query(Event)
        .filter(Event.event_date.year == year)
        .filter(Event.event_date.month == month)
        .filter(Event.is_deleted == False)
        .all()
    )

    return JSONResponse(
        content=[
            object_to_dict(EventRead.model_validate(event), format_date=True)
            for event in events
        ],
    )


@event_router.get(
    "/events/event_types",
    response_model=list[EventTypeRead],
    tags=["events"],
)
def read_event_types(
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read event types."""
    check_admin(current_user)

    event_types = db.query(EventType).filter(EventType.is_deleted.is_(False)).order_by(EventType.name).all()

    return JSONResponse(
        content=[
            object_to_dict(EventTypeRead.model_validate(event_type))
            for event_type in event_types
        ],
    )


@event_router.get(
    "/events/sub_event_types/{event_type_id}",
    response_model=list[EventRead],
    tags=["events"],
)
def read_sub_event_types(
    event_type_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read sub event types."""
    check_admin(current_user)

    event_sub_types = db.query(EventSubType).filter(EventSubType.event_type_id == event_type_id).filter(EventSubType.is_deleted.is_(False)).order_by(EventSubType.name).all()

    return JSONResponse(
        content=[
            object_to_dict(EventSubTypeRead.model_validate(event_sub_type))
            for event_sub_type in event_sub_types
        ],
    )