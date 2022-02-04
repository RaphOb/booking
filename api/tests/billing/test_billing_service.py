from booking.billing.model import Billing, BillingCreate, BillingUpdate
from booking.utils import crud_utils


def test_get_billing(session, billing):
    t_billing = crud_utils.read_one(
        model=Billing, record_id=billing.id, db_session=session
    )
    assert t_billing.id == billing.id


def test_gets_billing(session, billings):
    t_billings = crud_utils.read_all(model=Billing, db_session=session)
    assert len(t_billings) == len(billings)


def test_create_billing(session, reservation):
    from booking.billing.service import create

    t_billing = BillingCreate(bill=12, reservation_id=reservation.id, has_payed=True)
    billing = create(billing_in=t_billing, db_session=session)
    assert billing


def test_update_billing(session, billing):
    t_billing = BillingUpdate(bill=12, has_payed=True)
    billing = crud_utils.update(
        model=Billing, record=t_billing, record_id=billing.id, db_session=session
    )
    assert billing.bill == t_billing.bill


def test_delete_billing(session, billing):
    resp = crud_utils.delete(model=Billing, record_id=billing.id, db_session=session)
    assert resp == ("", 204)
