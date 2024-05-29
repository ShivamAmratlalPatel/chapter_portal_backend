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
from backend.utils import object_to_dict

update_router = APIRouter()

db_session = Depends(get_db)


@update_router.post(
    "/chapter_update", response_model=ChapterUpdateRead, tags=["updates"]
)
def create_chapter_update(
    chapter_update: ChapterUpdateCreate,
    db: Session = db_session,
) -> JSONResponse:
    """Create a chapter update."""
    chapter = db.get(Chapter, chapter_update.chapter_id)
    if chapter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found",
        )

    chapter_update = ChapterUpdate(**chapter_update.dict())
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
) -> JSONResponse:
    """Read a chapter update."""
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
) -> JSONResponse:
    """Update a chapter update."""
    existing_chapter_update: ChapterUpdate = db.get(ChapterUpdate, chapter_update_id)
    if existing_chapter_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter update not found",
        )

    existing_chapter_update.chapter_id = chapter_update.chapter_id
    existing_chapter_update.update_date = chapter_update.update_date
    existing_chapter_update.update_text = chapter_update.update_text

    db.add(existing_chapter_update)
    db.commit()

    return JSONResponse(
        content=object_to_dict(
            ChapterUpdateRead.model_validate(existing_chapter_update)
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
) -> None:
    """Delete a chapter update."""
    chapter_update = db.get(ChapterUpdate, chapter_update_id)
    if chapter_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter update not found",
        )

    chapter_update.is_deleted = True
    db.commit()

    return


@update_router.post(
    "/section_update", response_model=SectionUpdateRead, tags=["updates"]
)
def create_section_update(
    section_update: SectionUpdateCreate,
    db: Session = db_session,
) -> JSONResponse:
    """Create a section update."""
    section_update = SectionUpdate(**section_update.dict())
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
) -> JSONResponse:
    """Read a section update."""
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
) -> JSONResponse:
    """Update a section update."""
    existing_section_update = db.get(SectionUpdate, section_update_id)
    if existing_section_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section update not found",
        )

    existing_section_update.section_id = section_update.section_id
    existing_section_update.update_date = section_update.update_date
    existing_section_update.update_text = section_update.update_text

    db.add(existing_section_update)
    db.commit()

    return JSONResponse(
        content=object_to_dict(
            SectionUpdateRead.model_validate(existing_section_update)
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
) -> None:
    """Delete a section update."""
    section_update = db.get(SectionUpdate, section_update_id)
    if section_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section update not found",
        )

    section_update.is_deleted = True
    db.commit()

    return


@update_router.get(
    "/chapter_update/chapter/{chapter_id}",
    response_model=list[ChapterUpdateRead],
    tags=["updates"],
)
def read_chapter_updates(
    chapter_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Read all chapter updates for a chapter."""
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
) -> JSONResponse:
    """Read all section updates for a section."""
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
