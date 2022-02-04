from typing import List

from booking.categorie.model import Categorie, CategorieCreate, CategorieUpdate
from booking.utils import crud_utils


def test_get_categorie(session, categorie):
    t_categorie = crud_utils.read_one(
        model=Categorie, record_id=categorie.id, db_session=session
    )
    assert categorie.id == t_categorie.id


def test_get_all_categorie(session, categories: List[Categorie]):
    categorie_in = crud_utils.read_all(model=Categorie, db_session=session)
    assert len(categorie_in) == len(categories)


def test_create_categorie(session):
    from booking.categorie.service import create

    categorie_in = CategorieCreate(type=2, base_price=22.2, max_people=5)
    categorie = create(categorie_in=categorie_in, db_session=session)
    assert categorie


def test_update_categorie(session, categorie):
    categorie_in = CategorieUpdate(type=2, base_price=22.2, max_people=5)
    categorie_ = crud_utils.update(
        model=Categorie, record_id=categorie.id, record=categorie_in, db_session=session
    )
    assert categorie.base_price == categorie_.base_price


def test_delete_categorie(session, categorie):
    resp = crud_utils.delete(
        model=Categorie, record_id=categorie.id, db_session=session
    )
    assert resp == ("", 204)
