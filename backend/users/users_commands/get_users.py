"""Get user commands."""
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from backend.config import ALGORITHM, SECRET_KEY
from backend.helpers import get_db
from backend.users.users_models import User
from backend.users.users_schemas import TokenData, UserBase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

oauth2_scheme_depends = Depends(oauth2_scheme)
db_session = Depends(get_db)


def get_current_user(
    db: Session = db_session,
    token: str = oauth2_scheme_depends,
) -> UserBase:
    """Get current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    token_data = TokenData(username=username)
    user: User | None = get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return UserBase.model_validate(user)


current_user_depends = Depends(get_current_user)


def get_current_active_user(
    current_user: UserBase = current_user_depends,
) -> UserBase:
    """Get current active user."""
    if current_user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deleted user",
        )
    return current_user


def get_user_by_username(db: Session, username: str) -> User | None:
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user."""
    return db.query(User).filter(User.email == email).first()
