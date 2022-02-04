import logging

from fastapi import HTTPException

from ..billing.model import BillingCreate, Billing, BillingUpdate
from ..categorie.model import Categorie
from ..fluctuation.model import Fluctuation, ConditionState
from ..option.model import Option
from ..reservation.model import Reservation, ReservationRead
import pandas as pd

from ..utils import crud_utils

logger = logging.getLogger(__name__)


def create(*, billing_in: BillingCreate, db_session):
    billing = Billing(**billing_in.dict())
    db_session.add(billing)
    db_session.commit()
    return billing


def compute_bill(*, db_session, reservation_id):
    # get la reservation avec l'id et update la bill
    price_options = 0
    price_rooms = 0
    reservation = crud_utils.read_one(
        model=Reservation, record_id=reservation_id, db_session=db_session
    )
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    logger.info("start compute bill for resa n°: ".format(reservation.name_res))
    # get les optios -> nombre de jour   et prix => nb_jour *prix
    for option in reservation.reservationOptions:
        option_out = crud_utils.read_one(
            model=Option, record_id=option.option_id, db_session=db_session
        )
        price_options += option_out.price * option.nb_days
        logger.info("price for option:{} ".format(price_options))
    # get les rooms
    for room in reservation.rooms:
        room_categorie = crud_utils.read_one(
            model=Categorie, record_id=room.categorie_id, db_session=db_session
        )
        room_price = room_categorie.base_price
        logger.info("room price {}".format(room_price))
        date = pd.date_range(
            reservation.start_res, reservation.end_res, freq="D"
        ).to_series()
        # iterate entre la date de debut et la date de fin pour avoir le jour/
        # le fluctation rate et calculer le prix à la journée ( 0 = monday )
        for d in date.dt.dayofweek[:-1]:
            # Get fluctuation rate depend on day
            fluct = (
                db_session.query(Fluctuation)
                .filter(Fluctuation.condition == ConditionState(d + 1))
                .one_or_none()
            )
            rate = fluct.rate
            # check if special rate if one people in romm
            if reservation.nb_people == 1:
                fluct_alone = (
                    db_session.query(Fluctuation)
                    .filter(Fluctuation.condition == ConditionState(8))
                    .one_or_none()
                )
                rate += fluct_alone.rate
            price_rooms += room_price + (rate * room_price)

    total_price = price_rooms + price_options

    billing_model = BillingUpdate(
        bill=total_price,
    )
    billing = crud_utils.update(
        model=Billing,
        record=billing_model,
        record_id=reservation.billing.id,
        db_session=db_session,
    )
    return billing
