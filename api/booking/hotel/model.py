# sqlalchemy  schema
import uuid
from typing import List, Optional

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from ..database import Base
from ..models import TimeStampMixin, BookingBase
from ..room.model import RoomRead


class Hotel(Base, TimeStampMixin):
    # columns
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    city = Column(String(255))
    street = Column(String(255))
    nb_room = Column(Integer)
    nb_park = Column(Integer)
    nb_bb = Column(Integer)

    # relationships OneToMany
    rooms = relationship("Room", back_populates="hotel")


class HotelBase(BookingBase):
    name: str
    city: str
    street: str
    nb_room: int
    nb_park: int
    nb_bb: int


class HotelRead(HotelBase):
    id: uuid.UUID
    rooms: Optional[List[RoomRead]] = []


class HotelCreate(HotelBase):
    rooms: Optional[List[RoomRead]] = []


class HotelUpdate(HotelBase):
    pass
