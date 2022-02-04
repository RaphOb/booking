from booking.option.model import Option, OptionCreate, OptionUpdate
from booking.utils import crud_utils


def test_get_option(session, option):
    t_option = crud_utils.read_one(
        model=Option, record_id=option.id, db_session=session
    )
    assert t_option.id == option.id


def test_get_options(session, options):
    t_options = crud_utils.read_all(model=Option, db_session=session)
    assert len(t_options) == len(options)


def test_create_option(session):
    from booking.option.service import create

    t_option = OptionCreate(name="XXX", price=12, delay_before=2)
    option = create(option_in=t_option, db_session=session)
    assert option


def test_update_option(session, option):
    t_option = OptionUpdate(name="XXX", price=12, delay_before=2)
    option_out = crud_utils.update(
        model=Option, record=t_option, record_id=option.id, db_session=session
    )
    assert option_out.name == option.name


def test_delete_option(session, option):
    resp = crud_utils.delete(model=Option, record_id=option.id, db_session=session)
    assert resp == ("", 204)
