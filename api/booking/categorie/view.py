import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from .service import create
from ..database import get_db
from ..categorie.model import CategorieRead, Categorie, CategorieCreate, CategorieUpdate
from ..utils import crud_utils

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/categorie", tags=["categorie"], responses={404: {"categorie": "Not found"}}
)


@router.get("/{categorie_id}", response_model=CategorieRead)
def get(*, categorie_id: UUID, db: Session = Depends(get_db)):
    """Ge and categorie by id"""
    logger.info("Get categorie id: {}".format(categorie_id))
    data = crud_utils.read_one(model=Categorie, record_id=categorie_id, db_session=db)
    if data is None:
        logger.warning("Categorie Not Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.post("", response_model=CategorieRead, status_code=201)
def create_categorie(*, db: Session = Depends(get_db), categorie_in: CategorieCreate):
    """Create categorie"""
    logger.info("Create categorie : {}".format(categorie_in.type))
    return create(categorie_in=categorie_in, db_session=db)


@router.get("", response_model=List[CategorieRead])
def get_all(*, db: Session = Depends(get_db)):
    logger.info("Get All Categorie")
    data = crud_utils.read_all(model=Categorie, db_session=db)
    if data is None:
        logger.warning("Categories No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@router.delete("/{categorie_id}", status_code=204, response_class=Response)
def delete_categorie(*, categorie_id: UUID, db: Session = Depends(get_db)):
    resp = crud_utils.delete(model=Categorie, record_id=categorie_id, db_session=db)
    logger.info("Delete categorie id: {}".format(categorie_id))
    if resp is None:
        logger.info("Categories No Found")
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{categorie_id}", response_model=CategorieRead)
def update_categorie(
    *, categorie_id: UUID, categorie_in: CategorieUpdate, db: Session = Depends(get_db)
):
    logger.info("Update categorie  id: {}".format(categorie_id))
    resp = crud_utils.update(
        model=Categorie, record_id=categorie_id, record=categorie_in, db_session=db
    )
    if resp is None:
        logger.info("Categories No Found")
        raise HTTPException(status_code=404, detail="Item not found")
    return resp
