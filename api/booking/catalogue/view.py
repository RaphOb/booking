import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .service import generate_catalogue
from ..database import get_db
from ..catalogue.model import Catalogue

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/catalogue", tags=["catalogue"], responses={404: {"catalogue": "Not found"}}
)


@router.get("/", response_model=Catalogue)
def get(*, db: Session = Depends(get_db)):
    return generate_catalogue(db=db)
