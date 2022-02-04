from booking.reservation_option.model import (
    ReservationOption,
    ReservationOptionCreate,
    ReservationOptionUpdate,
)
from booking.utils import crud_utils


def test_get_ro(session, reservation_option):
    t_ro = crud_utils.read_one(
        model=ReservationOption, record_id=reservation_option.id, db_session=session
    )
    assert t_ro.id == reservation_option.id


def test_get_ros(session, reservation_options):
    t_ros = crud_utils.read_all(model=ReservationOption, db_session=session)
    assert len(t_ros) == len(reservation_options)


def test_create_ro(session, reservation, option):
    from booking.reservation_option.service import create

    t_ro_in = ReservationOptionCreate(
        reservation_id=reservation.id, option_id=option.id, nb_days=12
    )
    ro = create(reservation_option_in=t_ro_in, db_session=session)
    assert ro


def test_update_ro(session, reservation_option):
    t_ro_in = ReservationOptionUpdate(nb_days=11)
    ro = crud_utils.update(
        model=ReservationOption,
        record=t_ro_in,
        record_id=reservation_option.id,
        db_session=session,
    )
    assert ro.nb_days == reservation_option.nb_days


def test_delete_ro(session, reservation_option):
    resp = crud_utils.delete(
        model=ReservationOption, record_id=reservation_option.id, db_session=session
    )
    assert resp == ("", 204)
