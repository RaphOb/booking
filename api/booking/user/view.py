import logging
from datetime import timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from ..user.service import (
    create,
    authenticate_user,
    get_current_user,
    get_current_user_admin,
)
from ..database import get_db
from ..user.model import UserRead, UserCreate, User, UserUpdate
from ..utils import crud_utils
from ..utils.oauth_secu import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, Token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user", tags=["user"], responses={404: {"user": "Not found"}}
)


@router.post("", response_model=UserRead, status_code=201)
def create_user(*, db: Session = Depends(get_db), user_in: UserCreate):
    """Create user"""
    logger.info("Create user ")
    return create(user_in=user_in, db_session=db)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user_admin)):
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def get(*, user_id: UUID, db: Session = Depends(get_db)):
    """Ge and user by id"""
    logger.info("Get user id: {}".format(user_id))
    data = crud_utils.read_one(model=User, record_id=user_id, db_session=db)
    if data is None:
        logger.warning("User Not Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.get("", response_model=List[UserRead])
def get_all(*, db: Session = Depends(get_db)):
    logger.info("Get All User")
    data = crud_utils.read_all(model=User, db_session=db)
    if data is None:
        logger.warning("Users No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.delete("/{user_id}", status_code=204, response_class=Response)
def delete_user(*, user_id: UUID, db: Session = Depends(get_db)):
    resp = crud_utils.delete(model=User, record_id=user_id, db_session=db)
    logger.info("Delete user id: {}".format(user_id))
    if resp is None:
        logger.info("Users No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return None


@router.put("/{user_id}", response_model=UserRead)
def update_user(*, user_id: UUID, user_in: UserUpdate, db: Session = Depends(get_db)):
    logger.info("Update user  id: {}".format(user_id))
    resp = crud_utils.update(
        model=User, record_id=user_id, record=user_in, db_session=db
    )
    if resp is None:
        logger.info("Users No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return resp
