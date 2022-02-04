import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from .service import create
from ..database import get_db
from ..fluctuation.model import (
    FluctuationRead,
    Fluctuation,
    FluctuationCreate,
    FluctuationUpdate,
)
from ..utils import crud_utils

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/fluctuation",
    tags=["fluctuation"],
    responses={404: {"fluctuation": "Not found"}},
)


@router.get("/{fluctuation_id}", response_model=FluctuationRead)
def get(*, fluctuation_id: UUID, db: Session = Depends(get_db)):
    """Ge and fluctuation by id"""
    logger.info("Get fluctuation id: {}".format(fluctuation_id))
    data = crud_utils.read_one(
        model=Fluctuation, record_id=fluctuation_id, db_session=db
    )
    if data is None:
        logger.warning("Fluctuation Not Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.post("", response_model=FluctuationRead, status_code=201)
def create_fluctuation(
    *, db: Session = Depends(get_db), fluctuation_in: FluctuationCreate
):
    """Create fluctuation"""
    logger.info("Create fluctuation : {}".format(fluctuation_in.rate))
    return create(fluctuation_in=fluctuation_in, db_session=db)


@router.get("", response_model=List[FluctuationRead])
def get_all(*, db: Session = Depends(get_db)):
    logger.info("Get All Fluctuation")
    data = crud_utils.read_all(model=Fluctuation, db_session=db)
    if data is None:
        logger.warning("Fluctuations No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.delete("/{fluctuation_id}", status_code=204, response_class=Response)
def delete_fluctuation(*, fluctuation_id: UUID, db: Session = Depends(get_db)):
    resp = crud_utils.delete(model=Fluctuation, record_id=fluctuation_id, db_session=db)
    logger.info("Delete fluctuation id: {}".format(fluctuation_id))
    if resp is None:
        logger.info("Fluctuations No Found")
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{fluctuation_id}", response_model=FluctuationRead)
def update_fluctuation(
    *,
    fluctuation_id: UUID,
    fluctuation_in: FluctuationUpdate,
    db: Session = Depends(get_db)
):
    logger.info("Update fluctuation  id: {}".format(fluctuation_id))
    resp = crud_utils.update(
        model=Fluctuation,
        record_id=fluctuation_id,
        record=fluctuation_in,
        db_session=db,
    )
    if resp is None:
        logger.info("Fluctuations No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return resp
