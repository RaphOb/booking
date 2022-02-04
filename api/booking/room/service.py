from datetime import timedelta

from sqlalchemy.orm import aliased

from .model import Room, RoomCreate
from ..reservation.model import Reservation


def create(*, room_in: RoomCreate, db_session):
    room = Room(**room_in.dict())
    db_session.add(room)
    db_session.commit()
    return room


def if_reserved(*, room_number, date, db_session):
    reservation = aliased(Reservation)
    reserved = (
        db_session.query(Room)
        .join(reservation, Room.reservations)
        .filter(Room.number == room_number)
        .filter(reservation.start_res <= date + timedelta(days=1))
        .filter(reservation.end_res > date + timedelta(days=1))
        .one_or_none()
    )
    """
    Room -> Left Join Reservations -> 
    """

    return reserved
