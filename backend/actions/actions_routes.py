"""Endpoints for actions"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.actions.actions_models import Action
from backend.actions.actions_schemas import (
    ActionCreate,
    ActionRead,
    ActionUpdate,
    Assignee,
)
from backend.helpers import get_db
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_user_by_user_base import get_user_by_user_base
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_models import User, UserType
from backend.users.users_schemas import UserBase
from backend.utils import datetime_now, generate_uuid, object_to_dict

actions_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@actions_router.post(
    "/action",
    response_model=ActionRead,
    tags=["actions"],
)
def create_action(
    action: ActionCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create an action."""
    check_admin(current_user)

    user = get_user_by_user_base(current_user, db)

    assignee: User | None = (
        db.query(User)
        .filter(User.full_name == action.assignee_name)
        .order_by(User.created_date.desc())
        .first()
    )

    if assignee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignee not found",
        )

    action = Action(
        id=generate_uuid(),
        created_date=datetime_now(),
        section_id=action.section_id,
        chapter_id=action.chapter_id,
        note=action.note,
        due_date=action.due_date,
        created_user_id=user.id,
        assignee_id=assignee.id,
    )

    db.add(action)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(ActionRead.model_validate(action)),
    )


@actions_router.get(
    "/action/{action_id}",
    response_model=ActionRead,
    tags=["actions"],
)
def read_action(
    action_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read an action."""
    check_admin(current_user)

    action: Action | None = db.get(Action, action_id)

    if action is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(ActionRead.model_validate(action)),
    )


@actions_router.put(
    "/action/{action_id}",
    response_model=ActionRead,
    tags=["actions"],
)
def update_action(
    action_id: UUID,
    action: ActionUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update an action."""
    check_admin(current_user)

    action_instance: Action | None = db.get(Action, action_id)

    if action_instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found",
        )

    assignee: User | None = (
        db.query(User)
        .filter(User.full_name == action.assignee_name)
        .order_by(User.created_date.desc())
        .first()
    )

    if assignee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignee not found",
        )

    action_instance.section_id = action.section_id
    action_instance.chapter_id = action.chapter_id
    action_instance.note = action.note
    print(action.due_date)
    action_instance.due_date = action.due_date
    action_instance.assignee_id = assignee.id
    action_instance.completed_date = action.completed_date

    db.add(action_instance)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(ActionRead.model_validate(action_instance)),
    )


@actions_router.delete(
    "/action/{action_id}",
    tags=["actions"],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_action(
    action_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Delete an action."""
    check_admin(current_user)

    action: Action | None = db.get(Action, action_id)

    if action is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found",
        )

    action.is_deleted = True

    db.add(action)
    db.commit()


@actions_router.get(
    "/actions/chapter/{chapter_id}",
    response_model=list[ActionRead],
    tags=["actions"],
)
def read_actions_by_chapter(
    chapter_id: UUID,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read actions by chapter."""
    check_admin(current_user)

    actions: list[Action] = (
        db.query(Action)
        .filter(Action.chapter_id == chapter_id)
        .filter(Action.is_deleted.is_(False))
        .order_by(Action.due_date.desc())
        .all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(ActionRead.model_validate(action)) for action in actions
        ],
    )


@actions_router.get(
    "/actions/section/{section_id}",
    response_model=list[ActionRead],
    tags=["actions"],
)
def read_actions_by_section(
    section_id: int,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read actions by section."""
    check_admin(current_user)

    actions: list[Action] = (
        db.query(Action)
        .filter(Action.section_id == section_id)
        .filter(Action.is_deleted.is_(False))
        .order_by(Action.due_date.desc())
        .all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(ActionRead.model_validate(action)) for action in actions
        ],
    )


@actions_router.get(
    "/actions/me",
    response_model=list[ActionRead],
    tags=["actions"],
)
def read_my_actions(
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Read my actions."""
    user = get_user_by_user_base(current_user, db)

    actions: list[Action] = (
        db.query(Action)
        .filter(Action.assignee_id == user.id)
        .filter(Action.is_deleted.is_(False))
        .order_by(Action.due_date.desc())
        .all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(ActionRead.model_validate(action)) for action in actions
        ],
    )


@actions_router.get(
    "/actions/assignees",
    response_model=list[Assignee],
    tags=["actions"],
)
def get_assignees(
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
):
    check_admin(current_user)

    admin_user: UserType | None = (
        db.query(UserType).filter(UserType.name == "admin").first()
    )

    if admin_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin user not found",
        )

    assignees: list[User] = (
        db.query(User)
        .filter(User.is_deleted.is_(False))
        .filter(User.user_type_id == admin_user.id)
        .order_by(User.full_name.asc())
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            object_to_dict(Assignee.model_validate(assignee)) for assignee in assignees
        ],
    )
