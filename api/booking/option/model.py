import uuid
from typing import Optional, List

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .. import Base
from ..models import TimeStampMixin, BookingBase
from ..reservation_option.model import ReservationOptionRead


class Option(Base, TimeStampMixin):
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    price = Column(Float)
    delay_before = Column(Integer)

    # relation One ToMany
    reservationOptions = relationship("ReservationOption", back_populates="option")


class OptionBase(BookingBase):
    name: str
    price: float
    delay_before: int


class OptionCreate(OptionBase):
    reservationOptions: Optional[List[ReservationOptionRead]] = []


class OptionRead(OptionCreate):
    id: uuid.UUID


class OptionUpdate(OptionCreate):
    pass


class OptionReservation(BookingBase):
    id: uuid.UUID
    nb_days: int
