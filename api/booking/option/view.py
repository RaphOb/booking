import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from .service import create
from ..database import get_db
from ..option.model import OptionRead, Option, OptionCreate, OptionUpdate
from ..utils import crud_utils

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/option", tags=["option"], responses={404: {"option": "Not found"}}
)


@router.get("/{option_id}", response_model=OptionRead)
def get(*, option_id: UUID, db: Session = Depends(get_db)):
    """Ge and option by id"""
    logger.info("Get option id: {}".format(option_id))
    data = crud_utils.read_one(model=Option, record_id=option_id, db_session=db)
    if data is None:
        logger.warning("Option Not Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.post("", response_model=OptionRead, status_code=201)
def create_option(*, db: Session = Depends(get_db), option_in: OptionCreate):
    """Create option"""
    logger.info("Create option : {}".format(option_in.name))
    return create(option_in=option_in, db_session=db)


@router.get("", response_model=List[OptionRead])
def get_all(*, db: Session = Depends(get_db)):
    logger.info("Get All Option")
    data = crud_utils.read_all(model=Option, db_session=db)
    if data is None:
        logger.warning("Options No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.delete("/{option_id}", status_code=204, response_class=Response)
def delete_option(*, option_id: UUID, db: Session = Depends(get_db)):
    resp = crud_utils.delete(model=Option, record_id=option_id, db_session=db)
    logger.info("Delete option id: {}".format(option_id))
    if resp is None:
        logger.info("Options No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return None


@router.put("/{option_id}", response_model=OptionRead)
def update_option(
    *, option_id: UUID, option_in: OptionUpdate, db: Session = Depends(get_db)
):
    logger.info("Update option  id: {}".format(option_id))
    resp = crud_utils.update(
        model=Option, record_id=option_id, record=option_in, db_session=db
    )
    if resp is None:
        logger.info("Options No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return resp
