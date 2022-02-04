import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .. import Base
from ..billing.model import BillingRead
from ..models import TimeStampMixin, BookingBase
from ..option.model import OptionReservation
from ..reservation_option.model import ReservationOptionRead
from ..reservation_room.model import association_table
from ..room.model import RoomReservation


class Reservation(Base, TimeStampMixin):
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    start_res = Column(DateTime)
    end_res = Column(DateTime)
    name_res = Column(String(255))
    phone_res = Column(String(255))
    nb_people = Column(Integer)

    # Relation ManyToMany
    rooms = relationship(
        "Room", secondary=association_table, back_populates="reservations"
    )

    # Relation OneToMany
    reservationOptions = relationship("ReservationOption", back_populates="reservation")

    # Relation ManyToOne
    user_id = Column(UUIDType(binary=False), ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="reservations")

    # Relation OneToOne
    billing = relationship("Billing", back_populates="reservation", uselist=False)


class ReservationBase(BookingBase):
    start_res: datetime
    end_res: datetime
    name_res: str
    phone_res: str
    nb_people: int


class ReservationCreate(ReservationBase):
    user_id: uuid.UUID
    options: Optional[List[OptionReservation]]
    rooms: Optional[List[RoomReservation]]


class ReservationRead(ReservationCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    reservationOptions: Optional[List[ReservationOptionRead]] = []
    billing: BillingRead


class ReservationUpdate(ReservationBase):
    pass
