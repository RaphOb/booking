from booking.categorie.model import CategorieCreate, CategorieUpdate

CATEGORIE_URL = "/categorie"


def test_get_categorie(mock_categories, client):
    resp = client.get(CATEGORIE_URL + "/" + str(mock_categories[0].id))
    assert resp.status_code == 200


def test_get_categories(mock_categories, client):
    resp = client.get(CATEGORIE_URL)
    assert resp.status_code == 200
    assert len(resp.json()) == len(mock_categories)


def test_create_categorie(mock_categories, client):
    categorie_in = CategorieCreate(type=1, base_price=20.1, max_people=12)
    resp = client.post(
        CATEGORIE_URL,
        headers={"Content-Type": "application/json"},
        data=categorie_in.json(),
    )
    assert resp.status_code == 201


def test_update_categorie(mock_categories, client):
    categorie_in = CategorieUpdate(type=1, base_price=20.1, max_people=12)
    resp = client.put(
        CATEGORIE_URL + "/" + str(mock_categories[0].id),
        headers={"Content-Type": "application/json"},
        data=categorie_in.json(),
    )
    assert resp.status_code == 200


def test_delete_categorie(mock_categories, client):
    resp = client.delete(CATEGORIE_URL + "/" + str(mock_categories[0].id))
    assert resp.status_code == 204
