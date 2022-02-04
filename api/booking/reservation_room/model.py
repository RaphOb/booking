from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy_utils import UUIDType

from .. import Base

association_table = Table(
    "reservation_room",
    Base.metadata,
    Column("reservation_id", UUIDType(binary=False), ForeignKey("reservation.id")),
    Column("room_id", UUIDType(binary=False), ForeignKey("room.id")),
)
