import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from .service import create
from ..database import get_db
from ..room.model import (
    RoomRead,
    Room,
    RoomCreate,
    RoomUpdate,
    RoomAvailableIn,
    RoomAvailableOut,
)
from ..utils import crud_utils

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/room", tags=["room"], responses={404: {"room": "Not found"}}
)


@router.get("/{room_id}", response_model=RoomRead)
def get(*, room_id: UUID, db: Session = Depends(get_db)):
    """Ge and room by id"""
    logger.info("Get room id: {}".format(room_id))
    data = crud_utils.read_one(model=Room, record_id=room_id, db_session=db)
    if data is None:
        logger.warning("Room Not Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.post("", response_model=RoomRead, status_code=201)
def create_room(*, db: Session = Depends(get_db), room_in: RoomCreate):
    """Create room"""
    logger.info("Create room ")
    return create(room_in=room_in, db_session=db)


@router.get("", response_model=List[RoomRead])
def get_all(*, db: Session = Depends(get_db)):
    logger.info("Get All Room")
    data = crud_utils.read_all(model=Room, db_session=db)
    if data is None:
        logger.warning("Rooms No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.delete("/{room_id}", status_code=204, response_class=Response)
def delete_room(*, room_id: UUID, db: Session = Depends(get_db)):
    resp = crud_utils.delete(model=Room, record_id=room_id, db_session=db)
    logger.info("Delete room id: {}".format(room_id))
    if resp is None:
        logger.info("Rooms No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return None


@router.put("/{room_id}", response_model=RoomRead)
def update_room(*, room_id: UUID, room_in: RoomUpdate, db: Session = Depends(get_db)):
    logger.info("Update room  id: {}".format(room_id))
    resp = crud_utils.update(
        model=Room, record_id=room_id, record=room_in, db_session=db
    )
    if resp is None:
        logger.info("Rooms No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return resp


@router.get("/{room_id}/available", response_model=RoomAvailableOut)
def is_available(
    *, room_id: UUID, room_in: RoomAvailableIn, db: Session = Depends(get_db)
):
    query = """
        SELECT COUNT() FROM reservation_room
        LEFT JOIN reservation ON reservation_room.reservation_id = reservation.id
        WHERE 
            reservation_room.room_id = REPLACE(:room_id, "-", "")
        AND
            reservation.start_res BETWEEN :arrival AND :departure
        OR 
            reservation.end_res BETWEEN :arrival AND :departure
    """
    data = {
        "room_id": str(room_id),
        "arrival": str(room_in.arrival),
        "departure": str(room_in.departure),
    }

    result = db.execute(query, data).fetchone()

    if len(result) > 0:
        # Aucun chevauchement => Disponible
        if result[0] == 0:
            return {"available": True}
    return {"available": False}
