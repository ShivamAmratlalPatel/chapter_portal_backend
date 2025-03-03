"""Endpoints for committee"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.committees.commitee_schemas import CommitteeCreate, CommitteeRead
from backend.committees.committee_models import CommitteeMember
from backend.helpers import get_db
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_user_by_user_base import get_user_by_user_base
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_models import User
from backend.users.users_schemas import UserBase
from backend.utils import datetime_now, generate_uuid, object_to_dict

committee_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@committee_router.post(
    "/committee",
    response_model=CommitteeRead,
    tags=["committees"],
)
def create_committee(
    committee: CommitteeCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a committee."""
    check_admin(current_user)
    chapter = db.get(Chapter, committee.chapter_id)
    if chapter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found",
        )

    chapter_buddy: User | None = (
        db.query(User)
        .filter(User.full_name == committee.natcom_buddy_name)
        .order_by(User.created_date.desc())
        .first()
    )

    if chapter_buddy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignee not found",
        )

    committee = CommitteeMember(
        id=generate_uuid(),
        created_date=datetime_now(),
        name=committee.name,
        chapter_id=chapter.id,
        position=committee.position,
        email=committee.email,
        phone=committee.phone,
        commencement_date=committee.commencement_date,
        conclusion_date=committee.conclusion_date,
        natcom_buddy_id=chapter_buddy.id,
    )
    db.add(committee)
    db.commit()

    return JSONResponse(
        content=object_to_dict(CommitteeRead.model_validate(committee)),
    )


@committee_router.get(
    "/committee/{committee_id}",
    response_model=CommitteeRead,
    tags=["committees"],
)
def read_committee(
    committee_id: UUID,
    db: Session = db_session,
) -> JSONResponse:
    """Read a committee."""
    committee = db.get(CommitteeMember, committee_id)
    if committee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Committee not found",
        )

    return JSONResponse(
        content=object_to_dict(
            CommitteeRead.model_validate(committee),
            format_date=True,
        ),
    )


@committee_router.put(
    "/committee/{committee_id}",
    response_model=CommitteeRead,
    tags=["committees"],
)
def update_committee(
    committee_id: UUID,
    committee: CommitteeCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a committee."""
    check_admin(current_user)
    committee_db = db.get(CommitteeMember, committee_id)
    if committee_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Committee not found",
        )

    chapter_buddy: User | None = (
        db.query(User)
        .filter(User.full_name == committee.natcom_buddy_name)
        .order_by(User.created_date.desc())
        .first()
    )

    if chapter_buddy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignee not found",
        )

    committee_db.name = committee.name
    committee_db.chapter_id = committee.chapter_id
    committee_db.position = committee.position
    committee_db.email = committee.email
    committee_db.phone = committee.phone
    committee_db.commencement_date = committee.commencement_date
    committee_db.conclusion_date = committee.conclusion_date

    committee_db.natcom_buddy_id = chapter_buddy.id

    db.add(committee_db)
    db.commit()

    return JSONResponse(
        content=object_to_dict(CommitteeRead.model_validate(committee_db)),
    )


@committee_router.delete(
    "/committee/{committee_id}",
    tags=["committees"],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_committee(
    committee_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Delete a committee."""
    check_admin(current_user)
    committee = db.get(CommitteeMember, committee_id)
    if committee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Committee not found",
        )

    committee.is_deleted = True
    db.commit()


@committee_router.get(
    "/committee/chapter/{chapter_id}",
    response_model=list[CommitteeRead],
    tags=["committees"],
)
def read_committees_by_chapter(
    chapter_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read committees by chapter."""
    check_admin(current_user)

    committees: list[CommitteeMember] = (
        db.query(CommitteeMember)
        .filter_by(chapter_id=chapter_id)
        .filter_by(is_deleted=False)
        .all()
    )

    return JSONResponse(
        content=[
            object_to_dict(CommitteeRead.model_validate(committee), format_date=True)
            for committee in committees
        ],
    )


@committee_router.get(
    "/committee/chapter_buddy/me",
    response_model=list[CommitteeRead],
    tags=["committees"],
)
def read_committees_by_chapter_buddy(
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read committees by chapter buddy."""
    check_admin(current_user)

    user = get_user_by_user_base(current_user, db)

    committees: list[CommitteeMember] = (
        db.query(CommitteeMember)
        .filter_by(natcom_buddy_id=user.id)
        .filter_by(is_deleted=False)
        .all()
    )

    return JSONResponse(
        content=[
            object_to_dict(CommitteeRead.model_validate(committee), format_date=True)
            for committee in committees
        ],
    )
