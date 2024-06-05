"""Endpoints for health"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.health.health_models import ChapterHealth, HealthQuestion, Section
from backend.helpers import get_db
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import datetime_now, generate_uuid

health_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@health_router.get(
    "/health/{chapter_id}/year/{year}/month/{month}/week/{week}/question/{question_id}",
    tags=["chapter_health"],
)
def get_chapter_health(  # noqa: PLR0913
    chapter_id: UUID,
    year: int,
    month: int,
    week: int,
    question_id: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> int:
    """
    Get the health score for a chapter in a given month and year for a given question

    Args:
        chapter_id (UUID): The chapter id
        year (int): The year
        month (int): The month
        question_id (int): The question id
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        int: The health score

    """
    check_admin(current_user)
    chapter_health: ChapterHealth = (
        db.query(ChapterHealth)
        .join(HealthQuestion, ChapterHealth.health_question_id == HealthQuestion.id)
        .filter(ChapterHealth.chapter_id == chapter_id)
        .filter(ChapterHealth.year == year)
        .filter(ChapterHealth.month == month)
        .filter(ChapterHealth.week == week)
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
    current_user: UserBase = current_user_instance,
) -> list[dict]:
    """
    Get the health scores for a chapter by section

    Args:
        chapter_id (UUID): The chapter id
        section_id (int): The section id
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        list[dict]: The health scores

    """
    check_admin(current_user)
    periods: list[dict] = [
        {"year": 2024, "month": 6, "week": 1},
        {"year": 2024, "month": 6, "week": 3},
        {"year": 2024, "month": 7, "week": 1},
        {"year": 2024, "month": 7, "week": 3},
        {"year": 2024, "month": 8, "week": 1},
        {"year": 2024, "month": 8, "week": 3},
        {"year": 2024, "month": 9, "week": 1},
        {"year": 2024, "month": 9, "week": 3},
        {"year": 2024, "month": 10, "week": 1},
        {"year": 2024, "month": 10, "week": 3},
        {"year": 2024, "month": 11, "week": 1},
        {"year": 2024, "month": 11, "week": 3},
        {"year": 2024, "month": 12, "week": 1},
        {"year": 2024, "month": 12, "week": 3},
        {"year": 2025, "month": 1, "week": 1},
        {"year": 2025, "month": 1, "week": 3},
        {"year": 2025, "month": 2, "week": 1},
        {"year": 2025, "month": 2, "week": 3},
        {"year": 2025, "month": 3, "week": 1},
        {"year": 2025, "month": 3, "week": 3},
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
                .filter(ChapterHealth.week == period["week"])
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
    "/health/zone/{zone}/year/{year}/month/{month}/week/{week}/section/{section_id}",
    tags=["chapter_health"],
)
def get_chapter_health_by_section_and_period(  # noqa: PLR0913
    zone: str,
    year: int,
    month: int,
    week: int,
    section_id: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """
    Get the health scores for a chapter by section

    Args:
        zone (str): The zone
        year (int): The year
        month (int): The month
        section_id (int): The section id
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        list[dict]: The health scores

    """
    check_admin(current_user)
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
                .filter(ChapterHealth.week == week)
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
            output_dict["average"] = round(
                sum(
                    [
                        output_dict[question.id]
                        for question in questions
                        if output_dict[question.id] is not None
                        and isinstance(output_dict[question.id], int)
                    ],
                )
                / len(
                    [
                        question.id
                        for question in questions
                        if output_dict[question.id] is not None
                        and isinstance(output_dict[question.id], int)
                    ],
                ),
                2,
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
    current_user: UserBase = current_user_instance,
) -> None:
    """
    Update the health scores for a chapter

    Args:
        chapter_id (UUID): The chapter id
        data (dict): The health scores
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        None

    """
    check_admin(current_user)
    year = data.pop("year")
    month = data.pop("month")
    week = data.pop("week")

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
            .filter(ChapterHealth.week == week)
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
                score=score if score and score.isdigit() else None,
                comments=score if score is not None and not score.isdigit() else None,
            )

        db.add(chapter_health)
        db.commit()


@health_router.get("/sections", tags=["sections"])
def get_sections(
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """
    Get the sections

    Args:
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        list[Section]: The sections

    """
    check_admin(current_user)
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
def get_questions(
    section_id: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> list[dict]:
    """
    Get the questions for a section

    Args:
        section_id (int): The section id
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        list[dict]: The questions

    """
    check_admin(current_user)
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
        {"field": "week", "header": "week", "rag_guide": None},
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
def get_questions_by_section(
    section_id: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> list[dict]:
    """
    Get the questions for a section

    Args:
        section_id (int): The section id
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        list[dict]: The questions

    """
    check_admin(current_user)
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
def get_section(
    section_id: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """
    Get the section

    Args:
        section_id (int): The section id
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        list[Section]: The sections

    """
    check_admin(current_user)
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
    "/health/{chapter_id}/year/{year}/month/{month}/week/{week}/average",
    tags=["chapter_health"],
)
def get_average_chapter_health(
    chapter_id: UUID,
    year: int,
    month: int,
    week: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """
    Get the average health score for a chapter in a given month and year

    Args:
        chapter_id (UUID): The chapter id
        year (int): The year
        month (int): The month
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        int: The health score

    """
    check_admin(current_user)
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
                .filter(ChapterHealth.week == week)
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
    "/health/{chapter_id}/year/{year}/month/{month}/week/{week}/comments",
    tags=["chapter_health"],
)
def get_comments_chapter_health(
    chapter_id: UUID,
    year: int,
    month: int,
    week: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """
    Get the comments health score for a chapter in a given month and year

    Args:
        chapter_id (UUID): The chapter id
        year (int): The year
        month (int): The month
        db (Session, optional): The database session. Defaults to db_session.
        current_user (UserBase, optional): The current user. Defaults to current_user_instance.

    Returns:
        JSONResponse: The health comments
    """
    check_admin(current_user)
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
                .filter(ChapterHealth.week == week)
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
                    },
                )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=output,
    )


@health_router.get(
    "/health/{chapter_id}/latest",
    tags=["chapter_health"],
)
def get_chapter_latest_health(
    chapter_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
):
    check_admin(current_user)

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
            .filter(HealthQuestion.question.ilike("%Comments%").is_(False))
            .all()
        )

        health_scores = []
        for question in questions:
            chapter_health: ChapterHealth | None = (
                db.query(ChapterHealth)
                .filter(ChapterHealth.chapter_id == chapter_id)
                .filter(ChapterHealth.health_question_id == question.id)
                .filter(ChapterHealth.is_deleted.is_(False))
                .order_by(ChapterHealth.year.desc())
                .order_by(ChapterHealth.month.desc())
                .order_by(ChapterHealth.week.desc())
                .first()
            )

            if chapter_health:
                health_scores.append(chapter_health.score)

        output.append(
            {
                "section": section.name,
                "average": round(sum(health_scores) / len(health_scores), 2)
                if health_scores
                else None,
                "icon": section.icon,
            },
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=output,
    )
