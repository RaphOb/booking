import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .model import Agendas
from .service import generate_agendas
from ..database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/agendas", tags=["agendas"], responses={404: {"agendas": "Not found"}}
)


@router.post("")
def get(*, agenda_in: Agendas, db: Session = Depends(get_db)):
    return generate_agendas(agenda_in=agenda_in, db_session=db)
