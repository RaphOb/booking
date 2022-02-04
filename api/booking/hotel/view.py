import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from .service import create
from ..database import get_db
from ..hotel.model import HotelRead, Hotel, HotelCreate, HotelUpdate
from ..utils import crud_utils

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/hotel", tags=["hotel"], responses={404: {"hotel": "Not found"}}
)


@router.get("/{hotel_id}", response_model=HotelRead)
def get(*, hotel_id: UUID, db: Session = Depends(get_db)):
    """Ge and hotel by id"""
    logger.info("Get hotel id: {}".format(hotel_id))
    data = crud_utils.read_one(model=Hotel, record_id=hotel_id, db_session=db)
    if data is None:
        logger.warning("Hotel Not Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.post("", response_model=HotelRead, status_code=201)
def create_hotel(*, db: Session = Depends(get_db), hotel_in: HotelCreate):
    """Create hotel"""
    logger.info("Create hotel : {}".format(hotel_in.name))
    return create(hotel_in=hotel_in, db_session=db)


@router.get("", response_model=List[HotelRead])
def get_all(*, db: Session = Depends(get_db)):
    logger.info("Get All Hotel")
    data = crud_utils.read_all(model=Hotel, db_session=db)
    if data is None:
        logger.warning("Hotels No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.delete("/{hotel_id}", status_code=204, response_class=Response)
def delete_hotel(*, hotel_id: UUID, db: Session = Depends(get_db)):
    resp = crud_utils.delete(model=Hotel, record_id=hotel_id, db_session=db)
    logger.info("Delete hotel id: {}".format(hotel_id))
    if resp is None:
        logger.info("Hotels No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return None


@router.put("/{hotel_id}", response_model=HotelRead)
def update_hotel(
    *, hotel_id: UUID, hotel_in: HotelUpdate, db: Session = Depends(get_db)
):
    logger.info("Update hotel  id: {}".format(hotel_id))
    resp = crud_utils.update(
        model=Hotel, record_id=hotel_id, record=hotel_in, db_session=db
    )
    if resp is None:
        logger.info("Hotels No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return resp
