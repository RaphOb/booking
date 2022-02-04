import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from .service import create
from ..database import get_db
from ..reservation.model import (
    ReservationRead,
    Reservation,
    ReservationCreate,
    ReservationUpdate,
)
from ..utils import crud_utils

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/reservation",
    tags=["reservation"],
    responses={404: {"reservation": "Not found"}},
)


@router.get("/{reservation_id}", response_model=ReservationRead)
def get(*, reservation_id: UUID, db: Session = Depends(get_db)):
    """Ge and reservation by id"""
    logger.info("Get reservation id: {}".format(reservation_id))
    data = crud_utils.read_one(
        model=Reservation, record_id=reservation_id, db_session=db
    )
    if data is None:
        logger.warning("Reservation Not Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.post("", response_model=ReservationRead, status_code=201)
def create_reservation(
    *, db: Session = Depends(get_db), reservation_in: ReservationCreate
):
    """Create reservation"""
    logger.info("Create reservation ")
    return create(reservation_in=reservation_in, db_session=db)


@router.get("", response_model=List[ReservationRead])
def get_all(*, db: Session = Depends(get_db)):
    logger.info("Get All Reservation")
    data = crud_utils.read_all(model=Reservation, db_session=db)
    if data is None:
        logger.warning("Reservations No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.delete("/{reservation_id}", status_code=204, response_class=Response)
def delete_reservation(*, reservation_id: UUID, db: Session = Depends(get_db)):
    resp = crud_utils.delete(model=Reservation, record_id=reservation_id, db_session=db)
    logger.info("Delete reservation id: {}".format(reservation_id))
    if resp is None:
        logger.info("Reservations No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return None


@router.put("/{reservation_id}", response_model=ReservationRead)
def update_reservation(
    *,
    reservation_id: UUID,
    reservation_in: ReservationUpdate,
    db: Session = Depends(get_db)
):
    logger.info("Update reservation  id: {}".format(reservation_id))
    resp = crud_utils.update(
        model=Reservation,
        record_id=reservation_id,
        record=reservation_in,
        db_session=db,
    )
    if resp is None:
        logger.info("Reservations No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return resp
