"""Routes for users."""
from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from backend.chapters.chapters_models import Chapter
from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.helpers import get_db
from backend.users.users_commands.authenticate_user import authenticate_user
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_commands.password_token_commands import get_password_hash
from backend.users.users_commands.tokens import create_access_token
from backend.users.users_models import User, UserType
from backend.users.users_schemas import UserBase, UserCreate, UserCreateChapter
from backend.utils import generate_uuid

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)
form_instace = Depends()

users_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@users_router.post("/token", tags=["users"])
def login_for_access_token(
    db: Session = db_session,
    form_data: OAuth2PasswordRequestForm = form_instace,
) -> dict[str, str]:
    """Login for access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user.user_type_name},
        expires_delta=access_token_expires,
        chapter_id=user.chapter_id,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.post(
    "/users",
    tags=["users"],
    responses={
        status.HTTP_201_CREATED: {
            "description": "User created successfully",
        },
    },
)
def post_user(user_create: UserCreate, db: Session = db_session) -> JSONResponse:
    """Create user."""
    admin_user_id = db.query(UserType).filter(UserType.name == "admin").first().id
    user_already_exists = db.query(User).filter(User.email == user_create.email).first()
    if user_already_exists:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "email already exists"},
        )

    user = User(
        id=generate_uuid(),
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=get_password_hash(user_create.password),
        user_type_id=admin_user_id,
        is_deleted=True,
    )
    db.add(user)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created successfully"},
    )


@users_router.post(
    "/users/chapter",
    tags=["users"],
    responses={
        status.HTTP_201_CREATED: {
            "description": "User created successfully",
        },
    },
)
def post_user_chapter(
    user_create: UserCreateChapter,
    db: Session = db_session,
) -> JSONResponse:
    """Create chapter user."""
    user_already_exists = (
        db.query(User)
        .filter(
            User.email == user_create.email,
        )
        .first()
    )
    if user_already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    user_already_exists = (
        db.query(User)
        .filter(
            User.chapter_id == user_create.chapter_id,
        )
        .filter(User.is_deleted.is_(False))
        .first()
    )
    if user_already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only one chapter user is allowed per chapter",
        )

    chapter_type_id = db.query(UserType).filter(UserType.name == "chapter").first().id

    if chapter_type_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chapter type not found",
        )

    chapter = (
        db.query(Chapter)
        .filter(Chapter.id == user_create.chapter_id)
        .filter(Chapter.is_deleted.is_(False))
        .first()
    )

    if chapter is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chapter not found",
        )

    user = User(
        id=generate_uuid(),
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=get_password_hash(user_create.password),
        user_type_id=chapter_type_id,
        chapter_id=chapter.id,
        is_deleted=True,
    )
    db.add(user)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created successfully"},
    )


@users_router.get("/users/me", tags=["users"])
def get_me(
    current_user: UserBase = current_user_instance,
) -> UserBase:
    """Get current user."""
    return current_user


@users_router.get("/users", tags=["users"])
def get_all_users(
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> list[UserBase]:
    """Get all users."""
    check_admin(current_user)
    users = db.query(User).all()

    return [UserBase.model_validate(user) for user in users]


@users_router.put("/users/edit", tags=["users"])
def edit_user(
    full_name: str,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> None:
    """Edit user."""
    check_admin(current_user)
    user: User = db.query(User).filter(User.email == current_user.email).first()

    if user is None:
        user: User = db.query(User).filter(User.full_name == full_name).first()

    user.is_deleted = False

    db.add(user)

    db.commit()


@users_router.put(
    "/users/{user_id}/change_password",
    tags=["users"],
    status_code=status.HTTP_204_NO_CONTENT,
)
def change_password(
    user_id: UUID,
    password: str,
    db: Session = db_session,
) -> None:
    """Change password."""
    user: User = db.get(User, user_id)

    user.hashed_password = get_password_hash(password)

    db.add(user)

    db.commit()
