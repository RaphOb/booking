from ..reservation_option.model import ReservationOptionCreate, ReservationOption


def create(*, reservation_option_in: ReservationOptionCreate, db_session):
    ro_dict = reservation_option_in.dict()
    ro = ReservationOption(**ro_dict)
    db_session.add(ro)
    db_session.commit()
    return ro
