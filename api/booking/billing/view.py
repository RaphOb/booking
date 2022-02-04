import logging
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..billing.model import BillingRead
from ..billing.service import compute_bill
from ..database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/billing", tags=["billing"], responses={404: {"billing": "Not found"}}
)


@router.get("/{reservation_id}", response_model=BillingRead)
def get(*, reservation_id: UUID, db: Session = Depends(get_db)):
    """Ge and billing by id"""
    logger.info("Get billing id: {}".format("truc"))

    return compute_bill(db_session=db, reservation_id=reservation_id)
