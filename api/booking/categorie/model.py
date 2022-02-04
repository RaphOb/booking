import uuid
from enum import IntEnum
from typing import List, Optional

from sqlalchemy import Column, Integer, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from .. import Base
from ..models import TimeStampMixin, BookingBase
from ..room.model import RoomRead, RoomBase


class CategorieType(IntEnum):
    SR = 1
    S = 2
    JS = 3
    CD = 4
    CS = 5


class Categorie(Base, TimeStampMixin):
    # columns
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(CategorieType))
    base_price = Column(Float)
    max_people = Column(Integer)

    # relationships OneToMany
    rooms = relationship("Room", back_populates="categorie")


class CategorieBase(BookingBase):
    """ " Pydantic model"""

    type: CategorieType = CategorieType.CS
    base_price: float
    max_people: int


class CategorieRead(CategorieBase):
    id: uuid.UUID
    rooms: Optional[List[RoomRead]] = []


class CategorieCreate(CategorieBase):
    rooms: Optional[List[RoomBase]] = []


class CategorieUpdate(CategorieBase):
    pass
