from datetime import datetime

from booking.option.model import OptionReservation
from booking.reservation.model import Reservation, ReservationCreate, ReservationUpdate
from booking.room.model import RoomReservation
from booking.utils import crud_utils
import faker

fake = faker.Faker()


def test_get_reservation(session, reservation):
    t_reservation = crud_utils.read_one(
        model=Reservation, record_id=reservation.id, db_session=session
    )
    assert t_reservation.id == reservation.id


def test_get_reservations(session, reservations):
    t_reservation = crud_utils.read_all(model=Reservation, db_session=session)
    assert len(t_reservation) == len(reservations)


def test_create_reservation(session, user, rooms):
    from booking.reservation.service import create

    reservation_in = ReservationCreate(
        start_res=datetime.now(),
        end_res=datetime.now(),
        name_res=fake.name(),
        phone_res=fake.phone_number(),
        nb_people=12,
        user_id=user.id,
        rooms=[RoomReservation(id=rooms[0].id)],
    )

    reservation = create(reservation_in=reservation_in, db_session=session)

    assert reservation


def test_create_reservationwithoptions(session, options, user, rooms):
    from booking.reservation.service import create

    reservation_in = ReservationCreate(
        start_res=datetime.now(),
        end_res=datetime.now(),
        name_res=fake.name(),
        phone_res=fake.phone_number(),
        nb_people=12,
        user_id=user.id,
        rooms=[RoomReservation(id=rooms[0].id)],
        options=[
            OptionReservation(id=options[0].id, nb_days=12),
            OptionReservation(id=options[1].id, nb_days=10),
        ],
    )

    reservation = create(reservation_in=reservation_in, db_session=session)

    assert reservation
    assert reservation.reservationOptions[0].nb_days == 12
    assert reservation.reservationOptions[1].nb_days == 10


def test_create_reservationwithrooms(session, user, rooms):
    from booking.reservation.service import create

    reservation_in = ReservationCreate(
        start_res=datetime.now(),
        end_res=datetime.now(),
        name_res=fake.name(),
        phone_res=fake.phone_number(),
        nb_people=12,
        user_id=user.id,
        rooms=[RoomReservation(id=rooms[0].id)],
    )

    reservation = create(reservation_in=reservation_in, db_session=session)

    assert reservation


def test_update_reservation(session, reservation):
    reservation_in = ReservationUpdate(
        start_res=datetime.now(),
        end_res=datetime.now(),
        name_res=fake.name(),
        phone_res=fake.phone_number(),
        nb_people=12,
    )
    reservation = crud_utils.update(
        model=Reservation,
        record=reservation_in,
        record_id=reservation.id,
        db_session=session,
    )

    assert reservation.start_res == reservation_in.start_res


def test_delete_reservation(session, reservation):
    resp = crud_utils.delete(
        model=Reservation, record_id=reservation.id, db_session=session
    )
    assert resp == ("", 204)
