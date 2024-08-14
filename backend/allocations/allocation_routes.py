"""Endpoints for allocations"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.allocations.allocation_models import Allocation
from backend.allocations.allocation_schemas import AllocationCreate, AllocationRead
from backend.helpers import get_db
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_user_by_user_base import get_user_by_user_base
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_models import User
from backend.users.users_schemas import UserBase
from backend.utils import datetime_now, generate_uuid, object_to_dict

allocations_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@allocations_router.post(
    "/allocation",
    response_model=AllocationRead,
    tags=["allocations"],
)
def create_allocation(
    allocation: AllocationCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create an allocation."""
    check_admin(current_user)

    assignee: User | None = (
        db.query(User)
        .filter(User.full_name == allocation.user_name)
        .order_by(User.created_date.desc())
        .first()
    )

    if assignee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignee not found",
        )

    allocation = Allocation(
        id=generate_uuid(),
        created_date=datetime_now(),
        section_id=allocation.section_id,
        chapter_id=allocation.chapter_id,
        user_id=assignee.id,
    )

    db.add(allocation)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(AllocationRead.model_validate(allocation)),
    )


@allocations_router.get(
    "/allocation/{allocation_id}",
    response_model=AllocationRead,
    tags=["allocations"],
)
def read_allocation(
    allocation_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read an allocation."""
    check_admin(current_user)

    allocation: Allocation | None = db.get(Allocation, allocation_id)

    if allocation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allocation not found",
        )

    return JSONResponse(
        content=object_to_dict(AllocationRead.model_validate(allocation)),
    )


@allocations_router.put(
    "/allocation/{allocation_id}",
    response_model=AllocationRead,
    tags=["allocations"],
)
def update_allocation(
    allocation_id: UUID,
    allocation: AllocationCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update an allocation."""
    check_admin(current_user)

    allocation_instance: Allocation | None = db.get(Allocation, allocation_id)

    if allocation_instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allocation not found",
        )

    assignee: User | None = (
        db.query(User)
        .filter(User.full_name == allocation.user_name)
        .order_by(User.created_date.desc())
        .first()
    )

    if assignee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignee not found",
        )

    allocation_instance.section_id = allocation.section_id
    allocation_instance.chapter_id = allocation.chapter_id
    allocation_instance.user_id = assignee.id

    db.add(allocation_instance)
    db.commit()

    return JSONResponse(
        content=object_to_dict(AllocationRead.model_validate(allocation_instance)),
    )


@allocations_router.delete(
    "/allocation/{allocation_id}",
    response_model=AllocationRead,
    tags=["allocations"],
)
def delete_allocation(
    allocation_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete an allocation."""
    check_admin(current_user)

    allocation: Allocation | None = db.get(Allocation, allocation_id)

    if allocation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allocation not found",
        )

    allocation.is_deleted = True
    db.commit()

    return JSONResponse(
        content=object_to_dict(AllocationRead.model_validate(allocation)),
    )


@allocations_router.get(
    "/allocations/chapter/{chapter_id}",
    response_model=list[AllocationRead],
    tags=["allocations"],
)
def read_allocations_by_chapter(
    chapter_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read allocations by chapter."""
    check_admin(current_user)

    allocations: list[Allocation] = (
        db.query(Allocation)
        .filter_by(chapter_id=chapter_id)
        .filter_by(is_deleted=False)
        .all()
    )

    return JSONResponse(
        content=[
            object_to_dict(AllocationRead.model_validate(allocation))
            for allocation in allocations
        ],
    )


@allocations_router.get(
    "/allocations/me",
    response_model=list[AllocationRead],
    tags=["allocations"],
)
def read_my_allocations(
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read my allocations."""
    check_admin(current_user)
    user: User = get_user_by_user_base(current_user, db)

    allocations: list[Allocation] = (
        db.query(Allocation)
        .filter_by(user_id=user.id)
        .filter_by(is_deleted=False)
        .all()
    )

    return JSONResponse(
        content=[
            object_to_dict(AllocationRead.model_validate(allocation))
            for allocation in allocations
        ],
    )
