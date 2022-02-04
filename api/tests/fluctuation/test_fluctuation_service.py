from booking.fluctuation.model import Fluctuation, FluctuationCreate, FluctuationUpdate
from booking.utils import crud_utils


def test_get_fluctuation(session, fluctuation):
    t_fluctuation = crud_utils.read_one(
        model=Fluctuation, record_id=fluctuation.id, db_session=session
    )
    assert t_fluctuation.id == fluctuation.id


def test_get_fluctuations(session, fluctuations):
    t_fluctuations = crud_utils.read_all(model=Fluctuation, db_session=session)
    assert len(t_fluctuations) == len(fluctuations)


def test_create_fluctuation(session):
    from booking.fluctuation.service import create

    t_fluctuation = FluctuationCreate(condition=1, rate=0.12)
    fluctuation_out = create(fluctuation_in=t_fluctuation, db_session=session)
    assert fluctuation_out


def test_update_fluctuation(session, fluctuation):
    t_fluctuation = FluctuationUpdate(condition=2, rate=0.13)
    fluctuation_out = crud_utils.update(
        model=Fluctuation,
        record=t_fluctuation,
        record_id=fluctuation.id,
        db_session=session,
    )
    assert fluctuation_out.condition == fluctuation.condition


def test_delete_fluctuation(session, fluctuation):
    resp = crud_utils.delete(
        model=Fluctuation, record_id=fluctuation.id, db_session=session
    )
    assert resp == ("", 204)
