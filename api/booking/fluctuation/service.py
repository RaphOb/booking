from booking.fluctuation.model import Fluctuation


def create(*, fluctuation_in, db_session):
    fluctuation = Fluctuation(**fluctuation_in.dict())

    db_session.add(fluctuation)
    db_session.commit()

    return fluctuation
