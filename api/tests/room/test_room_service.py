from booking.room.model import Room, RoomCreate
from booking.utils import crud_utils


def test_get_file(session, room):
    t_room = crud_utils.read_one(model=Room, record_id=room.id, db_session=session)
    assert t_room.id == room.id


def test_get_all(session, hotel):
    t_rooms = crud_utils.read_all(model=Room, db_session=session)
    assert len(t_rooms) >= 1


def test_create_room(session, hotel, categorie):
    from booking.room.service import create

    room_in = RoomCreate(hotel_id=hotel.id, categorie_id=categorie.id, number=100)
    room = create(room_in=room_in, db_session=session)
    assert room


def test_delete_room(session, room):
    room = crud_utils.delete(model=Room, record_id=room.id, db_session=session)
    assert room == ("", 204)
