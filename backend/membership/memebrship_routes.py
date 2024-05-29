"""Endpoints for membership"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.helpers import get_db
from backend.membership.membership_models import MembershipLog
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict

membership_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@membership_router.get("/membership_log/{chapter_id}", tags=["membership"])
def get_membership_log(
    chapter_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Get membership log."""
    if current_user.chapter_id is not None:
        if current_user.chapter_id != chapter_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access to this chapter",
            )
    else:
        check_admin(current_user)
    chapter = db.get(Chapter, chapter_id)
    if chapter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found",
        )

    membership_log = (
        db.query(MembershipLog).filter(MembershipLog.chapter_id == chapter_id).all()
    )

    return JSONResponse(
        content={"membership_log": [object_to_dict(log) for log in membership_log]},
    )
