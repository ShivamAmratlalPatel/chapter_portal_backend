"""Endpoints for chapters"""
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.chapters.chapters_schemas import ChapterCreate, ChapterRead, ChapterUpdate
from backend.commands.get_paginated_result import GetPaginatedResult
from backend.helpers import get_db
from backend.schemas import PaginationResult, SortBy
from backend.utils import convert_list_to_list, object_to_dict

if TYPE_CHECKING:
    from sqlalchemy import Row

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


@chapters_router.get("/chapters", tags=["chapters"])
def list_chapters(  # noqa: PLR0913
    cursor_column: datetime | str | None = None,
    cursor_id: UUID | None = None,
    previous: bool | None = None,
    per_page: int | None = 20,
    filter_by: str | None = None,
    sort_by: SortBy | None = SortBy.date_asc,
    db: Session = db_session,
) -> PaginationResult:
    """Get all chapters."""
    pagination = GetPaginatedResult()

    filters = []

    if filter_by is not None and filter_by != "":
        filters.append(
            Chapter.name.ilike(f"%{filter_by}%"),
        )

    query = (
        db.query(Chapter)
        .filter(*filters)
        .filter(Chapter.is_deleted.is_(False))
        .order_by(
            pagination.get_sort_by(
                Chapter.name,
                Chapter.created_date,
                sort_by,
            ),
            Chapter.id.desc(),
        )
    )
    return pagination.run(
        cursor_id,
        cursor_column,
        previous,
        query,
        ChapterRead,
        per_page,
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


@chapters_router.get(
    "/all_chapters",
    tags=["chapters"],
    description="Get all chapters",
)
def list_all_chapters(
    db: Session = db_session,
) -> JSONResponse:
    """Get all chapters."""
    zones: list[Row] = (
        db.query(Chapter.zone).filter(Chapter.is_deleted.is_(False)).distinct()
    )

    output = []
    for zone in zones:
        chapters: list[Chapter] = (
            db.query(Chapter)
            .filter(Chapter.is_deleted.is_(False))
            .filter(Chapter.zone == zone[0])
            .all()
        )

        output.append(
            {
                "label": zone[0],
                "items": [
                    {
                        "label": chapter.name,
                        "icon": "pi pi-fw pi-id-card",
                        "to": f"/health/{chapter.id}",
                    }
                    for chapter in chapters
                ],
            },
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=convert_list_to_list(output, False),
    )
