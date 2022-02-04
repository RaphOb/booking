from typing import List

from booking.hotel.model import HotelCreate, Hotel, HotelUpdate
from booking.hotel.service import create
from booking.utils import crud_utils
import faker

fake = faker.Faker()


def test_create(session):
    name = "XXX"
    city = "XXX"
    street = "XXX"
    nb_room = 5
    nb_park = 2
    nb_bb = 4

    hotel_in = HotelCreate(
        name=name,
        city=city,
        street=street,
        nb_park=nb_park,
        nb_bb=nb_bb,
        nb_room=nb_room,
    )

    hotel = create(hotel_in=hotel_in, db_session=session)
    assert hotel


def test_get_hotel(session, hotel):
    t_hotel = crud_utils.read_one(model=Hotel, record_id=hotel.id, db_session=session)
    assert hotel.id == t_hotel.id


def test_get_all_hotels(session, hotels: List[Hotel]):
    hotels_in = crud_utils.read_all(model=Hotel, db_session=session)
    assert len(hotels_in) == len(hotels)


def test_update_hotel(session, hotel):
    hotel_in = HotelUpdate(
        name=fake.name(),
        city=fake.city(),
        street=fake.address(),
        nb_park=fake.random_int(min=1, max=15),
        nb_bb=fake.random_int(min=1, max=15),
        nb_room=fake.random_int(min=1, max=15),
    )
    hotel_out = crud_utils.update(
        model=Hotel, record_id=hotel.id, record=hotel_in, db_session=session
    )
    assert hotel_out.name == hotel_in.name
    assert hotel_out.city == hotel_in.city
    assert hotel_out.street == hotel_in.street
    assert hotel_out.nb_park == hotel_in.nb_park
    assert hotel_out.nb_bb == hotel_in.nb_bb
    assert hotel_out.nb_room == hotel_in.nb_room


def test_delete_hotel(session, hotel):
    crud_utils.delete(model=Hotel, record_id=hotel.id, db_session=session)
    hotel_in = crud_utils.read_one(model=Hotel, record_id=hotel.id, db_session=session)
    assert hotel_in is None
