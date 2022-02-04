import uuid
from enum import IntEnum
from typing import List, Optional
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .. import Base
from ..models import TimeStampMixin, BookingBase
from ..reservation.model import ReservationRead


class Role(IntEnum):
    ADMIN = 1
    USER = 2
    ANONYMOUS = 3


class User(Base, TimeStampMixin):
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    username = Column(String(16), unique=True)
    role = Column(Enum(Role))
    pwd_secure = Column(String(255))

    # relationships OneToMany
    reservations = relationship("Reservation", back_populates="user")


class UserBase(BookingBase):
    username: str
    role: Role = Role.ANONYMOUS


class UserCreate(UserBase):
    pwd_not_secure: str


class UserReadPwd(UserBase):
    id: uuid.UUID
    pwd_secure: str
    reservations: Optional[List[ReservationRead]] = []


class UserRead(UserBase):
    id: uuid.UUID
    reservations: Optional[List[ReservationRead]] = []


class UserUpdate(BookingBase):
    pass
