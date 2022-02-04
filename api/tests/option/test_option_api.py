from booking.option.model import OptionCreate, OptionUpdate

OPTION_URL = "/option"


def test_get_option(mock_options, client):
    resp = client.get(OPTION_URL + "/" + str(mock_options[0].id))
    assert resp.status_code == 200


def test_get_options(mock_options, client):
    resp = client.get(OPTION_URL)
    assert resp.status_code == 200
    assert len(resp.json()) == len(mock_options)


def test_create_option(mock_options, client):
    option_in = OptionCreate(name="xxx", price=1.2, delay_before=2)
    resp = client.post(
        OPTION_URL, headers={"Content-Type": "application/json"}, data=option_in.json()
    )
    assert resp.status_code == 201


def test_update_option(mock_options, client):
    option_in = OptionUpdate(name="xxx", price=1.2, delay_before=2)
    resp = client.put(
        OPTION_URL + "/" + str(mock_options[0].id),
        headers={"Content-Type": "application/json"},
        data=option_in.json(),
    )
    assert resp.status_code == 200


def test_delete_option(mock_options, client):
    resp = client.delete(OPTION_URL + "/" + str(mock_options[0].id))
    assert resp.status_code == 204
