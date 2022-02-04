from booking.fluctuation.model import FluctuationCreate

FLUCTUATION_URL = "/fluctuation"


def test_get_fluctuation(mock_fluctuations, client):
    response = client.get(FLUCTUATION_URL + "/" + str(mock_fluctuations[0].id))
    assert response.status_code == 200


def test_get_fluctuations(mock_fluctuations, client):
    response = client.get(FLUCTUATION_URL)
    assert response.status_code == 200


def test_create_fluctuation(mock_fluctuations, client):
    fluctuation_in = FluctuationCreate(condition=1, rate=0.1)

    resp = client.post(
        FLUCTUATION_URL,
        headers={"Content-Type": "application/json"},
        data=fluctuation_in.json(),
    )
    assert resp.status_code == 201


def test_update_fluctuation(mock_fluctuations, client):
    fluctuation_in = FluctuationCreate(condition=1, rate=0.1)
    resp = client.put(
        FLUCTUATION_URL + "/" + str(mock_fluctuations[0].id),
        headers={"Content-Type": "application/json"},
        data=fluctuation_in.json(),
    )
    assert resp.status_code == 200


def test_delete_fluctuation(mock_fluctuations, client):
    resp = client.delete(FLUCTUATION_URL + "/" + str(mock_fluctuations[0].id))
    assert resp.status_code == 204
