"""Endpoints for health"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from fastapi.responses import JSONResponse

from backend.chapters.chapters_models import Chapter
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

            period[question.id] = (
                chapter_health.score
                if chapter_health and chapter_health.score is not None
                else chapter_health.comments
                if chapter_health and chapter_health.comments
                else None
            )

    return periods


@health_router.get(
    "/health/zone/{zone}/year/{year}/month/{month}/section/{section_id}",
    tags=["chapter_health"],
)
def get_chapter_health_by_section_and_period(
    zone: str,
    year: int,
    month: int,
    section_id: int,
    db: Session = db_session,
) -> JSONResponse:
    """
    Get the health scores for a chapter by section

    Args:
        zone (str): The zone
        year (int): The year
        month (int): The month
        section_id (int): The section id
        db (Session, optional): The database session. Defaults to db_session.

    Returns:
        list[dict]: The health scores

    """
    chapters: list[Chapter] = (
        db.query(Chapter)
        .filter(Chapter.zone == zone)
        .filter(Chapter.is_deleted.is_(False))
        .order_by(Chapter.name)
        .all()
    )

    output = []

    questions = (
        db.query(HealthQuestion)
        .filter(HealthQuestion.section_id == section_id)
        .filter(HealthQuestion.is_deleted.is_(False))
        .all()
    )

    for chapter in chapters:
        output_dict = {
            "chapter_id": str(chapter.id),
            "chapter": chapter.name,
        }
        for question in questions:
            chapter_health: ChapterHealth = (
                db.query(ChapterHealth)
                .filter(ChapterHealth.chapter_id == chapter.id)
                .filter(ChapterHealth.year == year)
                .filter(ChapterHealth.month == month)
                .filter(ChapterHealth.is_deleted.is_(False))
                .filter(ChapterHealth.health_question_id == question.id)
                .order_by(ChapterHealth.created_date.desc())
                .first()
            )

            output_dict[question.id] = (
                chapter_health.score
                if chapter_health and chapter_health.score is not None
                else chapter_health.comments
                if chapter_health and chapter_health.comments
                else None
            )

        try:
            output_dict["average"] = sum(
                [
                    output_dict[question.id]
                    for question in questions
                    if output_dict[question.id] is not None
                    and isinstance(output_dict[question.id], int)
                ]
            ) / len(
                [
                    question.id
                    for question in questions
                    if output_dict[question.id] is not None
                    and isinstance(output_dict[question.id], int)
                ]
            )
        except ZeroDivisionError:
            output_dict["average"] = None

        output.append(output_dict)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=output,
    )


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
            # check if score is a string representation of an integer
            if isinstance(score, int) or score.isdigit():
                chapter_health.score = int(score)
            else:
                chapter_health.comments = score
            chapter_health.last_modified_date = datetime_now()
        else:
            chapter_health = ChapterHealth(
                id=generate_uuid(),
                chapter_id=chapter_id,
                year=year,
                month=month,
                health_question_id=db_question.id,
                score=score if score.isdigit() else None,
                comments=score if not score.isdigit() else None,
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
        content=[
            {"id": section.id, "name": section.name, "is_deleted": section.is_deleted}
            for section in sections
        ],
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
        {"field": "year", "header": "year", "rag_guide": None},
        {"field": "month", "header": "month", "rag_guide": None},
    ] + [
        {
            "field": str(question.id),
            "header": question.question,
            "rag_guide": question.rag_guide,
            "overlay_panel": False,
        }
        for question in questions
    ]


@health_router.get("/questions/section/{section_id}/section", tags=["questions"])
def get_questions_by_section(section_id: int, db: Session = db_session) -> list[dict]:
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

    return (
        [
            {"field": "chapter", "header": "chapter", "rag_guide": None},
        ]
        + [
            {
                "field": str(question.id),
                "header": question.question,
                "rag_guide": question.rag_guide,
                "overlay_panel": False,
            }
            for question in questions
        ]
        + [{"field": "average", "header": "average", "rag_guide": None}]
    )


@health_router.get("/section/{section_id}", tags=["sections"])
def get_section(section_id: int, db: Session = db_session) -> JSONResponse:
    """
    Get the section

    Args:
        section_id (int): The section id
        db (Session, optional): The database session. Defaults to db_session.

    Returns:
        list[Section]: The sections

    """
    section: Section = (
        db.query(Section)
        .filter(Section.id == section_id)
        .filter(Section.is_deleted.is_(False))
        .order_by(Section.id)
        .first()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": section.id,
            "name": section.name,
            "is_deleted": section.is_deleted,
        },
    )


@health_router.get(
    "/health/{chapter_id}/year/{year}/month/{month}/average", tags=["chapter_health"]
)
def get_average_chapter_health(
    chapter_id: UUID,
    year: int,
    month: int,
    db: Session = db_session,
) -> JSONResponse:
    """
    Get the average health score for a chapter in a given month and year

    Args:
        chapter_id (UUID): The chapter id
        year (int): The year
        month (int): The month
        db (Session, optional): The database session. Defaults to db_session.

    Returns:
        int: The health score

    """
    sections: list[Section] = (
        db.query(Section)
        .filter(Section.is_deleted.is_(False))
        .order_by(Section.id)
        .all()
    )

    output = []

    for section in sections:
        sum_average = 0
        sum_count = 0

        questions: list[HealthQuestion] = (
            db.query(HealthQuestion)
            .filter(HealthQuestion.section_id == section.id)
            .filter(HealthQuestion.is_deleted.is_(False))
            .all()
        )

        for question in questions:
            chapter_health: ChapterHealth = (
                db.query(ChapterHealth)
                .filter(ChapterHealth.chapter_id == chapter_id)
                .filter(ChapterHealth.year == year)
                .filter(ChapterHealth.month == month)
                .filter(ChapterHealth.is_deleted.is_(False))
                .filter(ChapterHealth.health_question_id == question.id)
                .order_by(ChapterHealth.created_date.desc())
                .first()
            )

            if chapter_health:
                sum_average += (
                    chapter_health.score if chapter_health.score is not None else 0
                )
                sum_count += 1

        try:
            average = sum_average / sum_count
        except ZeroDivisionError:
            average = None

        output.append(average)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=output,
    )


@health_router.get(
    "/health/{chapter_id}/year/{year}/month/{month}/comments", tags=["chapter_health"]
)
def get_comments_chapter_health(
    chapter_id: UUID,
    year: int,
    month: int,
    db: Session = db_session,
) -> JSONResponse:
    """
    Get the comments health score for a chapter in a given month and year

    Args:
        chapter_id (UUID): The chapter id
        year (int): The year
        month (int): The month
        db (Session, optional): The database session. Defaults to db_session.

    Returns:
        JSONResponse: The health comments
    """
    sections: list[Section] = (
        db.query(Section)
        .filter(Section.is_deleted.is_(False))
        .order_by(Section.id)
        .all()
    )

    output = []

    for section in sections:
        questions: list[HealthQuestion] = (
            db.query(HealthQuestion)
            .filter(HealthQuestion.section_id == section.id)
            .filter(HealthQuestion.is_deleted.is_(False))
            .filter(HealthQuestion.question.ilike("%Comments%"))
            .all()
        )

        for question in questions:
            chapter_health: ChapterHealth = (
                db.query(ChapterHealth)
                .filter(ChapterHealth.chapter_id == chapter_id)
                .filter(ChapterHealth.year == year)
                .filter(ChapterHealth.month == month)
                .filter(ChapterHealth.is_deleted.is_(False))
                .filter(ChapterHealth.health_question_id == question.id)
                .order_by(ChapterHealth.created_date.desc())
                .first()
            )

            if chapter_health:
                output.append(
                    {
                        "section": section.name,
                        "comment": chapter_health.comments
                        if chapter_health.comments
                        else None,
                    }
                )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=output,
    )
