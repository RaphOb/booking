from booking.room.model import RoomCreate, RoomUpdate

ROOM_URL = "/room"


def test_get_room(mock_rooms, client):
    resp = client.get(ROOM_URL + "/" + str(mock_rooms[0].id))
    assert resp.status_code == 200


def test_get_rooms(mock_rooms, client):
    resp = client.get(ROOM_URL)
    assert resp.status_code == 200
    assert len(resp.json()) == len(mock_rooms)


def test_create_room(mock_rooms, client, hotel, categorie):
    room_in = RoomCreate(
        hotel_id=hotel.id, categorie_id=categorie.id, number=mock_rooms[0].number
    )
    resp = client.post(
        ROOM_URL, headers={"Content-Type": "application/json"}, data=room_in.json()
    )
    assert resp.status_code == 201


def test_update_room(mock_rooms, client, categorie):
    room_in = RoomUpdate(categorie_id=categorie.id, number=mock_rooms[0].number)
    resp = client.put(
        ROOM_URL + "/" + str(mock_rooms[0].id),
        headers={"Content-Type": "application/json"},
        data=room_in.json(),
    )
    assert resp.status_code == 200


def test_delete_room(mock_rooms, client):
    resp = client.delete(ROOM_URL + "/" + str(mock_rooms[0].id))
    assert resp.status_code == 204
