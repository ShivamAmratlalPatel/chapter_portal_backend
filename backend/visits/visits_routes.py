"""Endpoints for Visits"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_user_by_user_base import get_user_by_user_base
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import datetime_now, generate_uuid
from backend.visits.visits_models import ChapterVisitAssociation, Visit
from backend.visits.visits_schemas import VisitCreate, VisitRead

visit_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@visit_router.post("/visit", response_model=VisitRead, tags=["visits"])
def create_visit(
    visit: VisitCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> VisitRead:
    """Create a new visit"""
    check_admin(current_user)

    user = get_user_by_user_base(current_user, db)

    chapter_visit: Visit = Visit(
        id=generate_uuid(),
        created_date=datetime_now(),
        is_deleted=False,
        visit_date=visit.visit_date,
        user_id=user.id,
        visit_category_id=visit.visit_category_id,
        comments=visit.comments,
    )

    db.add(chapter_visit)
    db.commit()

    for chapter_id in visit.chapter_ids:
        chapter_visit_association = ChapterVisitAssociation(
            id=generate_uuid(),
            is_deleted=False,
            chapter_id=chapter_id,
            visit_id=chapter_visit.id,
        )
        db.add(chapter_visit_association)
        db.commit()

    return VisitRead.model_validate(chapter_visit)


@visit_router.get("/visit/{visit_id}", response_model=VisitRead, tags=["visits"])
def get_visit(
    visit_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> VisitRead:
    """Get a visit"""
    check_admin(current_user)

    visit: Visit | None = db.get(Visit, visit_id)

    if visit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found",
        )

    return VisitRead.model_validate(visit)


@visit_router.put("/visit/{visit_id}", response_model=VisitRead, tags=["visits"])
def update_visit(
    visit_id: UUID,
    visit: VisitCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> VisitRead:
    """Update a visit"""
    check_admin(current_user)

    visit_instance: Visit | None = db.get(Visit, visit_id)

    if visit_instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found",
        )

    user = get_user_by_user_base(current_user, db)

    if visit_instance.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden to edit another visit",
        )

    visit_instance.visit_date = visit.visit_date
    visit_instance.visit_category_id = visit.visit_category_id
    visit_instance.comments = visit.comments

    visit_instance.chapter_visit_associations = []

    for chapter_id in visit.chapter_ids:
        chapter_visit_association = ChapterVisitAssociation(
            id=generate_uuid(),
            is_deleted=False,
            chapter_id=chapter_id,
            visit_id=visit_instance.id,
        )
        db.add(chapter_visit_association)
        db.commit()

    db.add(visit_instance)
    db.commit()

    return VisitRead.model_validate(visit_instance)


@visit_router.delete(
    "/visit/{visit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["visits"],
)
def delete_visit(
    visit_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Delete a visit"""
    check_admin(current_user)

    visit: Visit | None = db.get(Visit, visit_id)

    if visit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found",
        )

    visit.is_deleted = True

    db.add(visit)
    db.commit()


@visit_router.get(
    "/visits/chapter/{chapter_id}",
    response_model=list[VisitRead],
    tags=["visits"],
)
def get_visits_by_chapter(
    chapter_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> list[VisitRead]:
    """Get visits by chapter"""
    check_admin(current_user)

    visits: list[Visit] = (
        db.query(Visit)
        .join(ChapterVisitAssociation)
        .filter(
            ChapterVisitAssociation.chapter_id == chapter_id,
            ChapterVisitAssociation.is_deleted.is_(False),
            Visit.is_deleted.is_(False),
        )
        .all()
    )

    return [VisitRead.model_validate(visit) for visit in visits]
