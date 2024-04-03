"""Ednpoints for chapters"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.chapters.chapters_schemas import ChapterCreate, ChapterRead, ChapterUpdate
from backend.helpers import get_db
from backend.utils import object_to_dict

chapters_router = APIRouter()

db_session = Depends(get_db)


@chapters_router.post(
    "/chapter",
    tags=["chapters"],
    description="Create chapter.",
    responses={
        status.HTTP_201_CREATED: {
            "model": ChapterRead,
            "description": "Successful response: chapter created",
            "title": "Chapter details",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Chapter already exists",
            "title": "Chapter already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Chapter already exists"},
                },
            },
        },
    },
)
def create_chapter(
    chapter_details: ChapterCreate,
    db: Session = db_session,
) -> JSONResponse:
    """Create a chapter."""
    try:
        chapter = Chapter(**chapter_details.model_dump())
        db.add(chapter)
        db.commit()
        db.refresh(chapter)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Chapter already exists",
        ) from e
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(ChapterRead.model_validate(chapter)),
    )


@chapters_router.get(
    "/chapter/{chapter_id}",
    tags=["chapters"],
    description="Get chapter.",
    responses={
        status.HTTP_200_OK: {
            "model": ChapterRead,
            "description": "Successful response: chapter found",
            "title": "Chapter details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Chapter not found",
            "title": "Chapter not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Chapter not found"},
                },
            },
        },
    },
)
def get_chapter(
    chapter_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Get a chapter."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(ChapterRead.model_validate(chapter)),
    )


@chapters_router.get(
    "/chapters",
    tags=["chapters"],
    description="Get chapters.",
    responses={
        status.HTTP_200_OK: {
            "model": list[ChapterRead],
            "description": "Successful response: chapters found",
            "title": "Chapter details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Chapters not found",
            "title": "Chapters not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Chapters not found"},
                },
            },
        },
    },
)
def get_chapters(
    db: Session = db_session,
) -> JSONResponse:
    """Get all chapters."""
    chapters = db.query(Chapter).all()
    if not chapters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapters not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(ChapterRead.model_validate(chapter)) for chapter in chapters
        ],
    )


@chapters_router.put(
    "/chapter/{chapter_id}",
    tags=["chapters"],
    description="Update chapter.",
    responses={
        status.HTTP_200_OK: {
            "model": ChapterRead,
            "description": "Successful response: chapter updated",
            "title": "Chapter details",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Chapter not found",
            "title": "Chapter not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Chapter not found"},
                },
            },
        },
    },
)
def update_chapter(
    chapter_id: UUID,
    chapter_details: ChapterUpdate,
    db: Session = db_session,
) -> JSONResponse:
    """Update a chapter."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found",
        )
    for field, value in chapter_details:
        setattr(chapter, field, value)
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(ChapterRead.model_validate(chapter)),
    )


@chapters_router.delete(
    "/chapter/{chapter_id}",
    tags=["chapters"],
    description="Delete chapter.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful response: chapter deleted",
            "title": "Chapter deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Chapter not found",
            "title": "Chapter not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Chapter not found"},
                },
            },
        },
    },
)
def delete_chapter(
    chapter_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Delete a chapter."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found",
        )
    chapter.is_deleted = True
    db.add(chapter)
    db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
