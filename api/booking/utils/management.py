import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db, Base

from typing import List

from ..categorie.model import CategorieCreate, CategorieType
from ..fluctuation.model import FluctuationCreate, ConditionState
from ..hotel.model import HotelCreate
from ..option.model import OptionCreate
from ..room.model import RoomCreate, RoomReservation
from ..option.model import OptionReservation
from ..reservation.model import ReservationCreate
from ..user.model import UserCreate
from .. import hotel, categorie, room, option, fluctuation, reservation, user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/management", tags=["management"])


@router.get("/")
def restart(session: Session = Depends(get_db)):
    tables = Base.metadata.sorted_tables
    for table in tables:
        print("clear table: {}".format(table))
        session.execute(table.delete())
    session.commit()

    #     Create Hotel 1
    hotel_1_in = HotelCreate(
        name="Hotel 1",
        city="Paris",
        street="12 rue truc",
        nb_room=5,
        nb_park=3,
        nb_bb=2,
    )
    hotel_1 = hotel.service.create(hotel_in=hotel_1_in, db_session=session)

    # Create Hotel 2
    hotel_2_in = HotelCreate(
        name="Hotel 2",
        city="Biarritz",
        street="65 rue de la plage",
        nb_room=2,
        nb_park=2,
        nb_bb=2,
    )
    hotel_2 = hotel.service.create(hotel_in=hotel_2_in, db_session=session)

    # Create Categorie
    cat_1_in = CategorieCreate(type=CategorieType.CS, base_price=150, max_people=2)
    cat_2_in = CategorieCreate(type=CategorieType.CD, base_price=300, max_people=2)
    cat_3_in = CategorieCreate(type=CategorieType.JS, base_price=500, max_people=2)
    cat_4_in = CategorieCreate(type=CategorieType.S, base_price=720, max_people=3)
    cat_5_in = CategorieCreate(type=CategorieType.SR, base_price=1000, max_people=5)
    cat_1 = categorie.service.create(categorie_in=cat_1_in, db_session=session)
    cat_2 = categorie.service.create(categorie_in=cat_2_in, db_session=session)
    cat_3 = categorie.service.create(categorie_in=cat_3_in, db_session=session)
    cat_4 = categorie.service.create(categorie_in=cat_4_in, db_session=session)
    cat_5 = categorie.service.create(categorie_in=cat_5_in, db_session=session)

    # Create Room for Hotel 1
    room_1_1_in = RoomCreate(hotel_id=hotel_1.id, categorie_id=cat_4.id, number=100)
    room_1_2_in = RoomCreate(hotel_id=hotel_1.id, categorie_id=cat_3.id, number=101)
    room_1_3_in = RoomCreate(hotel_id=hotel_1.id, categorie_id=cat_2.id, number=102)
    room_1_4_in = RoomCreate(hotel_id=hotel_1.id, categorie_id=cat_1.id, number=103)
    room_1_5_in = RoomCreate(hotel_id=hotel_1.id, categorie_id=cat_1.id, number=104)

    # Create Room for Hotel2
    room_2_1_in = RoomCreate(hotel_id=hotel_2.id, categorie_id=cat_5.id, number=200)
    room_2_2_in = RoomCreate(hotel_id=hotel_2.id, categorie_id=cat_5.id, number=201)

    room_1_1 = room.service.create(room_in=room_1_1_in, db_session=session)
    room_1_2 = room.service.create(room_in=room_1_2_in, db_session=session)
    room_1_3 = room.service.create(room_in=room_1_3_in, db_session=session)
    room_1_4 = room.service.create(room_in=room_1_4_in, db_session=session)
    room_1_5 = room.service.create(room_in=room_1_5_in, db_session=session)
    room_2_1 = room.service.create(room_in=room_2_1_in, db_session=session)
    room_2_1 = room.service.create(room_in=room_2_2_in, db_session=session)

    # Create Options
    option_1_in = OptionCreate(name="parking", price=25, delay_before=0)
    option_2_in = OptionCreate(name="lit bébé", price=0, delay_before=0)
    option_3_in = OptionCreate(name="romance", price=50, delay_before=2)
    option_4_in = OptionCreate(name="bf", price=30, delay_before=0)

    option_1 = option.service.create(option_in=option_1_in, db_session=session)
    option_2 = option.service.create(option_in=option_2_in, db_session=session)
    option_3 = option.service.create(option_in=option_3_in, db_session=session)
    option_4 = option.service.create(option_in=option_4_in, db_session=session)

    # create Fluctuation
    fluctuation_1_in = FluctuationCreate(condition=ConditionState.Monday, rate=0)
    fluctuation_2_in = FluctuationCreate(condition=ConditionState.Tuesday, rate=0)
    fluctuation_3_in = FluctuationCreate(condition=ConditionState.Wednesday, rate=-0.10)
    fluctuation_4_in = FluctuationCreate(condition=ConditionState.Thursday, rate=-0.10)
    fluctuation_5_in = FluctuationCreate(condition=ConditionState.Friday, rate=0.15)
    fluctuation_6_in = FluctuationCreate(condition=ConditionState.Saturday, rate=0.15)
    fluctuation_7_in = FluctuationCreate(condition=ConditionState.Sunday, rate=0)
    fluctuation_8_in = FluctuationCreate(condition=ConditionState.ALONE, rate=-0.05)

    fluctuation_1 = fluctuation.service.create(
        fluctuation_in=fluctuation_1_in, db_session=session
    )
    fluctuation_2 = fluctuation.service.create(
        fluctuation_in=fluctuation_2_in, db_session=session
    )
    fluctuation_3 = fluctuation.service.create(
        fluctuation_in=fluctuation_3_in, db_session=session
    )
    fluctuation_4 = fluctuation.service.create(
        fluctuation_in=fluctuation_4_in, db_session=session
    )
    fluctuation_5 = fluctuation.service.create(
        fluctuation_in=fluctuation_5_in, db_session=session
    )
    fluctuation_6 = fluctuation.service.create(
        fluctuation_in=fluctuation_6_in, db_session=session
    )
    fluctuation_7 = fluctuation.service.create(
        fluctuation_in=fluctuation_7_in, db_session=session
    )
    fluctuation_8 = fluctuation.service.create(
        fluctuation_in=fluctuation_8_in, db_session=session
    )

    # Create Admin User 1
    user_1_in = UserCreate(username="hourli_a", role=1, pwd_not_secure="password")
    # Create Non Admin User 2
    user_2_in = UserCreate(username="obadia_r", role=2, pwd_not_secure="password")
    user_1 = user.service.create(user_in=user_1_in, db_session=session)
    user_2 = user.service.create(user_in=user_2_in, db_session=session)

    # Create Reservations
    reservation_1_1_in = ReservationCreate(
        user_id=user_1.id,
        options=[OptionReservation(id=option_1.id, nb_days=1)],
        rooms=[RoomReservation(id=room_1_1.id)],
        start_res="2021-06-23 13:00:00.000000",
        end_res="2021-06-24 13:00:00.000000",
        name_res="Dubois",
        phone_res="06528175282",
        nb_people=5,
    )
    reservation_1_2_in = ReservationCreate(
        user_id=user_2.id,
        options=[
            OptionReservation(id=option_2.id, nb_days=3),
            OptionReservation(id=option_3.id, nb_days=2),
            OptionReservation(id=option_4.id, nb_days=2),
        ],
        rooms=[
            RoomReservation(id=room_1_2.id),
            RoomReservation(id=room_1_3.id),
            RoomReservation(id=room_1_4.id),
        ],
        start_res="2021-06-23 16:00:00.000000",
        end_res="2021-06-30 10:00:00.000000",
        name_res="Arcka",
        phone_res="0655132382",
        nb_people=2,
    )
    reservation_1 = reservation.service.create(
        reservation_in=reservation_1_1_in, db_session=session
    )
    reservation_2 = reservation.service.create(
        reservation_in=reservation_1_2_in, db_session=session
    )
