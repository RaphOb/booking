from pydantic import BaseModel

from typing import List, Optional, Dict

from ..hotel.model import HotelBase
from ..room.model import RoomBase
from ..categorie.model import CategorieBase
from ..fluctuation.model import FluctuationBase


class CategoryCatalogue(CategorieBase):
    pass


class RoomCatalogue(RoomBase):
    categorie: CategoryCatalogue


class HotelCatalogue(HotelBase):
    rooms: Optional[List[RoomCatalogue]] = []


class Catalogue(BaseModel):
    hotels: List[HotelCatalogue]
    fluctuations: List[FluctuationBase]
