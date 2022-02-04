from ..billing.model import Billing
from ..reservation.model import ReservationCreate, Reservation
from ..reservation_option.model import ReservationOptionCreate, ReservationOption
from ..room.model import Room


def create(*, reservation_in: ReservationCreate, db_session) -> Reservation:
    reservation_dict = reservation_in.dict()
    options_dict = reservation_dict.pop("options", [])
    rooms_dict = reservation_dict.pop("rooms", [])

    reservation = Reservation(**reservation_dict)

    for room in rooms_dict:
        r = db_session.query(Room).filter(Room.id == room["id"]).one_or_none()
        reservation.rooms.append(r)

    db_session.add(reservation)

    # init Billing
    billing_in = Billing(reservation_id=reservation.id, bill=0, has_payed=False)
    db_session.add(billing_in)
    reservation.billing = billing_in
    db_session.commit()
    add_option_reservation(
        options=options_dict, reservation_id=reservation.id, db_session=db_session
    )
    return reservation


def add_option_reservation(*, options, reservation_id, db_session):
    """Create option_reservation with Optionid and Reservation id"""
    if options:
        for option in options:
            option_reservation_in = ReservationOptionCreate(
                option_id=option["id"],
                reservation_id=reservation_id,
                nb_days=option["nb_days"],
            )
            option_reservation = ReservationOption(**option_reservation_in.dict())
            db_session.add(option_reservation)
        db_session.commit()
