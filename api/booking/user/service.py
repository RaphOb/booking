from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from booking.user.model import UserCreate, User, Role
from ..database import get_db
from ..utils.oauth_secu import (
    verify_password,
    get_password_hash,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
    TokenData,
)


def authenticate_user(db, username: str, password: str):
    user = read_by_name(username=username, db_session=db)
    if not user:
        return False
    if not verify_password(password, user.pwd_secure):
        return False
    return user


def read_by_name(*, username, db_session) -> User:
    return db_session.query(User).filter(User.username == username).one_or_none()


def create(*, user_in: UserCreate, db_session) -> User:
    # hash pwd
    if user_in.pwd_not_secure:
        pass_hash = get_password_hash(user_in.pwd_not_secure)

        user = User(username=user_in.username, role=user_in.role, pwd_secure=pass_hash)

        db_session.add(user)
        db_session.commit()
        return user


def get_current_user(
    db_session: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = read_by_name(username=token_data.username, db_session=db_session)
    if user is None:
        raise credentials_exception
    return user


def get_current_user_admin(
    db_session: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = read_by_name(username=token_data.username, db_session=db_session)
    if user is None:
        raise credentials_exception
    if user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
