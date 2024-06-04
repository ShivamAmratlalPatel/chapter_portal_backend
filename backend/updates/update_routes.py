"""Endpoints for Updates"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.helpers import get_db
from backend.updates.updates_models import ChapterUpdate, SectionUpdate
from backend.updates.updates_schemas import (
    ChapterUpdateCreate,
    ChapterUpdateRead,
    SectionUpdateCreate,
    SectionUpdateRead,
)
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_user_by_user_base import get_user_by_user_base
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict, generate_uuid

update_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@update_router.post(
    "/chapter_update",
    response_model=ChapterUpdateRead,
    tags=["updates"],
)
def create_chapter_update(
    chapter_update: ChapterUpdateCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a chapter update."""
    check_admin(current_user)

    user = get_user_by_user_base(current_user, db)

    chapter = db.get(Chapter, chapter_update.chapter_id)
    if chapter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found",
        )

    chapter_update = ChapterUpdate(
        id=generate_uuid(), **chapter_update.dict(), user_id=user.id
    )
    db.add(chapter_update)
    db.commit()

    return JSONResponse(
        content=object_to_dict(ChapterUpdateRead.model_validate(chapter_update)),
    )


@update_router.get(
    "/chapter_update/{chapter_update_id}",
    response_model=ChapterUpdateRead,
    tags=["updates"],
)
def read_chapter_update(
    chapter_update_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read a chapter update."""
    check_admin(current_user)
    chapter_update = db.get(ChapterUpdate, chapter_update_id)
    if chapter_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter update not found",
        )

    return JSONResponse(
        content=object_to_dict(ChapterUpdateRead.model_validate(chapter_update)),
    )


@update_router.put(
    "/chapter_update/{chapter_update_id}",
    response_model=ChapterUpdateRead,
    tags=["updates"],
)
def update_chapter_update(
    chapter_update_id: UUID,
    chapter_update: ChapterUpdateCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a chapter update."""
    check_admin(current_user)
    existing_chapter_update: ChapterUpdate = db.get(ChapterUpdate, chapter_update_id)
    if existing_chapter_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter update not found",
        )

    user = get_user_by_user_base(current_user, db)

    if user.id != existing_chapter_update.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not have permission to update this chapter update",
        )

    existing_chapter_update.chapter_id = chapter_update.chapter_id
    existing_chapter_update.update_date = chapter_update.update_date
    existing_chapter_update.update_text = chapter_update.update_text

    db.add(existing_chapter_update)
    db.commit()

    return JSONResponse(
        content=object_to_dict(
            ChapterUpdateRead.model_validate(existing_chapter_update),
        ),
    )


@update_router.delete(
    "/chapter_update/{chapter_update_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["updates"],
)
def delete_chapter_update(
    chapter_update_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Delete a chapter update."""
    check_admin(current_user)
    chapter_update = db.get(ChapterUpdate, chapter_update_id)
    if chapter_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter update not found",
        )

    chapter_update.is_deleted = True
    db.commit()


@update_router.post(
    "/section_update",
    response_model=SectionUpdateRead,
    tags=["updates"],
)
def create_section_update(
    section_update: SectionUpdateCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a section update."""
    check_admin(current_user)
    user = get_user_by_user_base(current_user, db)
    section_update = SectionUpdate(
        id=generate_uuid(), **section_update.dict(), user_id=user.id
    )
    db.add(section_update)
    db.commit()

    return JSONResponse(
        content=object_to_dict(SectionUpdateRead.model_validate(section_update)),
    )


@update_router.get(
    "/section_update/{section_update_id}",
    response_model=SectionUpdateRead,
    tags=["updates"],
)
def read_section_update(
    section_update_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read a section update."""
    check_admin(current_user)
    section_update = db.get(SectionUpdate, section_update_id)
    if section_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section update not found",
        )

    return JSONResponse(
        content=object_to_dict(SectionUpdateRead.model_validate(section_update)),
    )


@update_router.put(
    "/section_update/{section_update_id}",
    response_model=SectionUpdateRead,
    tags=["updates"],
)
def update_section_update(
    section_update_id: UUID,
    section_update: SectionUpdateCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a section update."""
    check_admin(current_user)
    existing_section_update = db.get(SectionUpdate, section_update_id)
    if existing_section_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section update not found",
        )

    user = get_user_by_user_base(current_user, db)

    if user.id != existing_section_update.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not have permission to update this section update",
        )

    existing_section_update.section_id = section_update.section_id
    existing_section_update.update_date = section_update.update_date
    existing_section_update.update_text = section_update.update_text

    db.add(existing_section_update)
    db.commit()

    return JSONResponse(
        content=object_to_dict(
            SectionUpdateRead.model_validate(existing_section_update),
        ),
    )


@update_router.delete(
    "/section_update/{section_update_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["updates"],
)
def delete_section_update(
    section_update_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Delete a section update."""
    check_admin(current_user)
    section_update = db.get(SectionUpdate, section_update_id)
    if section_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section update not found",
        )

    section_update.is_deleted = True
    db.commit()


@update_router.get(
    "/chapter_update/chapter/{chapter_id}",
    response_model=list[ChapterUpdateRead],
    tags=["updates"],
)
def read_chapter_updates(
    chapter_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read all chapter updates for a chapter."""
    check_admin(current_user)
    chapter = db.get(Chapter, chapter_id)
    if chapter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found",
        )

    chapter_updates = (
        db.query(ChapterUpdate)
        .filter_by(chapter_id=chapter_id)
        .filter_by(is_deleted=False)
        .all()
    )

    return JSONResponse(
        content=[
            object_to_dict(ChapterUpdateRead.model_validate(chapter_update))
            for chapter_update in chapter_updates
        ],
    )


@update_router.get(
    "/section_update/section/{section_id}",
    response_model=list[SectionUpdateRead],
    tags=["updates"],
)
def read_section_updates(
    section_id: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read all section updates for a section."""
    check_admin(current_user)
    section_updates = (
        db.query(SectionUpdate)
        .filter_by(section_id=section_id)
        .filter_by(is_deleted=False)
        .all()
    )

    return JSONResponse(
        content=[
            object_to_dict(SectionUpdateRead.model_validate(section_update))
            for section_update in section_updates
        ],
    )
