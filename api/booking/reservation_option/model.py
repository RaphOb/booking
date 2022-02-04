import uuid

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .. import Base
from ..models import TimeStampMixin, BookingBase


class ReservationOption(Base, TimeStampMixin):
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    nb_days = Column(Integer)

    # Relation ManyToOne
    reservation_id = Column(
        UUIDType(binary=False), ForeignKey("reservation.id", ondelete="CASCADE")
    )
    option_id = Column(
        UUIDType(binary=False), ForeignKey("option.id", ondelete="CASCADE")
    )
    reservation = relationship("Reservation", back_populates="reservationOptions")
    option = relationship("Option", back_populates="reservationOptions")


class ReservationOptionBase(BookingBase):
    nb_days: int


class ReservationOptionCreate(ReservationOptionBase):
    reservation_id: uuid.UUID
    option_id: uuid.UUID


class ReservationOptionRead(ReservationOptionCreate):
    id: uuid.UUID


class ReservationOptionUpdate(ReservationOptionBase):
    pass
