from datetime import datetime
import uuid

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from ..database import Base
from ..models import TimeStampMixin, BookingBase
from ..reservation_room.model import association_table


class Room(Base, TimeStampMixin):
    # columns
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    number = Column(Integer, nullable=False, unique=True)

    # relations ManyToOne
    hotel_id = Column(
        UUIDType(binary=False), ForeignKey("hotel.id", ondelete="CASCADE")
    )
    hotel = relationship("Hotel", back_populates="rooms")
    categorie = relationship("Categorie", back_populates="rooms")
    categorie_id = Column(
        UUIDType(binary=False), ForeignKey("categorie.id", ondelete="CASCADE")
    )

    # relations ManyToMany
    reservations = relationship(
        "Reservation", secondary=association_table, back_populates="rooms"
    )


class RoomBase(BookingBase):
    """Base Pydantic"""

    number: int
    pass


class RoomRead(RoomBase):
    id: uuid.UUID
    hotel_id: uuid.UUID
    categorie_id: uuid.UUID
    number: int


class RoomCreate(RoomBase):
    hotel_id: uuid.UUID
    categorie_id: uuid.UUID
    number: int


class RoomUpdate(RoomBase):
    pass


class RoomAvailableIn(RoomBase):
    arrival: datetime
    departure: datetime


class RoomAvailableOut(RoomBase):
    available: bool


class RoomReservation(BookingBase):
    id: uuid.UUID
