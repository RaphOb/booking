import uuid
from enum import IntEnum

from sqlalchemy import Column, Enum, Float
from sqlalchemy_utils import UUIDType

from .. import Base
from ..models import TimeStampMixin, BookingBase


class ConditionState(IntEnum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7
    ALONE = 8


class Fluctuation(Base, TimeStampMixin):
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    condition = Column(Enum(ConditionState))
    rate = Column(Float)


class FluctuationBase(BookingBase):
    """Pydantic model"""

    condition: ConditionState = ConditionState.Monday
    rate: float


class FluctuationCreate(FluctuationBase):
    pass


class FluctuationRead(FluctuationBase):
    id: uuid.UUID


class FluctuationUpdate(FluctuationBase):
    pass
