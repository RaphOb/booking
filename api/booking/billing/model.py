import uuid

from sqlalchemy import Column, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .. import Base
from ..models import TimeStampMixin, BookingBase


class Billing(Base, TimeStampMixin):
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    bill = Column(Float)
    has_payed = Column(Boolean)

    # Relation OneToOne
    reservation_id = Column(UUIDType(binary=False), ForeignKey("reservation.id"))
    reservation = relationship("Reservation", back_populates="billing")


class BillingBase(BookingBase):
    bill: float
    has_payed: bool = False


class BillingCreate(BillingBase):
    reservation_id: uuid.UUID


class BillingRead(BillingCreate):
    id: uuid.UUID


class BillingUpdate(BillingBase):
    pass
