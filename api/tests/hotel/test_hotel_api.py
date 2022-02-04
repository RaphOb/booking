from booking.hotel.model import HotelCreate, HotelUpdate

HOTEL_URL = "/hotel"


def test_get_hotel(client, mock_hotels):
    url = HOTEL_URL + "/" + str(mock_hotels[0].id)
    response = client.get(url)
    assert response.status_code == 200


def test_create_hotel(client, mock_hotels):
    hotel_in = HotelCreate(
        name="name",
        city="Gig",
        street="street",
        nb_park=12,
        nb_bb=12,
        nb_room=12,
    )
    response = client.post(
        HOTEL_URL, headers={"Content-Type": "application/json"}, data=hotel_in.json()
    )
    assert response.status_code == 201


def test_get_hotels(client, mock_hotels):
    response = client.get(HOTEL_URL)
    assert response.status_code == 200


def test_update_hotel(client, mock_hotels):
    hotel_in = HotelUpdate(
        name="name",
        city="city",
        street="street",
        nb_park=12,
        nb_bb=12,
        nb_room=12,
    )
    response = client.put(
        HOTEL_URL + "/" + str(mock_hotels[0].id),
        headers={"Content-Type": "application/json"},
        data=hotel_in.json(),
    )
    assert response.status_code == 200


def test_delete_hotel(client, mock_hotels):
    url = HOTEL_URL + "/" + str(mock_hotels[0].id)
    resp = client.delete(url)
    assert resp.status_code == 204
    url = HOTEL_URL + "/" + str(mock_hotels[1].id)
    resp1 = client.delete(url)
    assert resp1.status_code == 204
