"""Endpoints for health"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from fastapi.responses import JSONResponse

from backend.health.health_models import ChapterHealth, HealthQuestion, Section
from backend.helpers import get_db
from backend.utils import datetime_now, generate_uuid

health_router = APIRouter()

db_session = Depends(get_db)


@health_router.get(
    "/health/{chapter_id}/year/{year}/month/{month}/question/{question_id}",
    tags=["chapter_health"],
)
def get_chapter_health(
    chapter_id: UUID,
    year: int,
    month: int,
    question_id: int,
    db: Session = db_session,
) -> int:
    """
    Get the health score for a chapter in a given month and year for a given question

    Args:
        chapter_id (UUID): The chapter id
        year (int): The year
        month (int): The month
        question_id (int): The question id
        db (Session, optional): The database session. Defaults to db_session.

    Returns:
        int: The health score

    """
    chapter_health: ChapterHealth = (
        db.query(ChapterHealth)
        .join(HealthQuestion, ChapterHealth.health_question_id == HealthQuestion.id)
        .filter(ChapterHealth.chapter_id == chapter_id)
        .filter(ChapterHealth.year == year)
        .filter(ChapterHealth.month == month)
        .filter(ChapterHealth.health_question_id == question_id)
        .filter(HealthQuestion.is_deleted.is_(False))
        .filter(ChapterHealth.is_deleted.is_(False))
        .order_by(ChapterHealth.created_date.desc())
    ).first()

    return chapter_health.score if chapter_health else None


@health_router.get(
    "/health/{chapter_id}/section/{section_id}",
    tags=["chapter_health"],
)
def get_chapter_health_by_section(
    chapter_id: UUID,
    section_id: int,
    db: Session = db_session,
) -> list[dict]:
    """
    Get the health scores for a chapter by section

    Args:
        chapter_id (UUID): The chapter id
        section_id (int): The section id
        db (Session, optional): The database session. Defaults to db_session.

    Returns:
        list[dict]: The health scores

    """
    periods: list[dict] = [
        {"year": 2024, "month": 4},
        {"year": 2024, "month": 5},
        {"year": 2024, "month": 6},
        {"year": 2024, "month": 7},
        {"year": 2024, "month": 8},
        {"year": 2024, "month": 9},
        {"year": 2024, "month": 10},
        {"year": 2024, "month": 11},
        {"year": 2024, "month": 12},
        {"year": 2025, "month": 1},
        {"year": 2025, "month": 2},
        {"year": 2025, "month": 3},
    ]

    questions: list[HealthQuestion] = (
        db.query(HealthQuestion)
        .filter(HealthQuestion.is_deleted.is_(False))
        .filter(HealthQuestion.section_id == section_id)
        .all()
    )

    for period in periods:
        for question in questions:
            chapter_health: ChapterHealth = (
                db.query(ChapterHealth)
                .filter(ChapterHealth.chapter_id == chapter_id)
                .filter(ChapterHealth.year == period["year"])
                .filter(ChapterHealth.month == period["month"])
                .filter(ChapterHealth.health_question_id == question.id)
                .filter(ChapterHealth.is_deleted.is_(False))
                .order_by(ChapterHealth.created_date.desc())
            ).first()

            period[question.id] = chapter_health.score if chapter_health else None

    return periods


@health_router.put(
    "/health/{chapter_id}",
    tags=["chapter_health"],
)
def update_chapter_health(
    chapter_id: UUID,
    data: dict,
    db: Session = db_session,
) -> None:
    """
    Update the health scores for a chapter

    Args:
        chapter_id (UUID): The chapter id
        data (dict): The health scores
        db (Session, optional): The database session. Defaults to db_session.

    Returns:
        None

    """
    year = data.pop("year")
    month = data.pop("month")

    for question, score in data.items():
        db_question: HealthQuestion = (
            db.query(HealthQuestion)
            .filter(HealthQuestion.id == int(question))
            .filter(HealthQuestion.is_deleted.is_(False))
            .first()
        )

        if not db_question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question {question} not found",
            )

        chapter_health: ChapterHealth = (
            db.query(ChapterHealth)
            .filter(ChapterHealth.chapter_id == chapter_id)
            .filter(ChapterHealth.year == year)
            .filter(ChapterHealth.month == month)
            .filter(ChapterHealth.health_question_id == db_question.id)
            .filter(ChapterHealth.is_deleted.is_(False))
            .order_by(ChapterHealth.created_date.desc())
        ).first()

        if chapter_health:
            chapter_health.score = int(score)
            chapter_health.last_modified_date = datetime_now()
        else:
            chapter_health = ChapterHealth(
                id=generate_uuid(),
                chapter_id=chapter_id,
                year=year,
                month=month,
                health_question_id=db_question.id,
                score=score,
            )

        db.add(chapter_health)
        db.commit()


@health_router.get("/sections", tags=["sections"])
def get_sections(db: Session = db_session) -> JSONResponse:
    """
    Get the sections

    Args:
        db (Session, optional): The database session. Defaults to db_session.

    Returns:
        list[Section]: The sections

    """
    sections: list[Section] = (
        db.query(Section)
        .filter(Section.is_deleted.is_(False))
        .order_by(Section.id)
        .all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[{"id": section.id, "name": section.name} for section in sections],
    )


@health_router.get("/questions/section/{section_id}", tags=["questions"])
def get_questions(section_id: int, db: Session = db_session) -> list[dict]:
    """
    Get the questions for a section

    Args:
        section_id (int): The section id
        db (Session, optional): The database session. Defaults to db_session.

    Returns:
        list[dict]: The questions

    """
    questions: list[HealthQuestion] = (
        db.query(HealthQuestion)
        .filter(HealthQuestion.is_deleted.is_(False))
        .filter(HealthQuestion.section_id == section_id)
        .order_by(HealthQuestion.id)
        .all()
    )

    return [
        {"field": "year", "header": "year"},
        {"field": "month", "header": "month"},
    ] + [
        {"field": str(question.id), "header": question.question}
        for question in questions
    ]
