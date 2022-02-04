from datetime import datetime

from booking.agendas.model import Agendas

AGENDAS_URL = "/agendas"


def test_get_categorie(mock_agendas, client):
    agendas_in = Agendas(
        start=datetime.now(),
        end=datetime.now(),
    )
    resp = client.post(
        AGENDAS_URL,
        headers={"Content-Type": "application/json"},
        data=agendas_in.json(),
    )
    assert resp.status_code == 200
    assert type(resp.json()) == dict
