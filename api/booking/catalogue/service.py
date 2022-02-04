from .model import Catalogue
from ..hotel.model import Hotel
from ..room.model import Room
from ..categorie.model import Categorie
from ..fluctuation.model import Fluctuation
from ..utils import crud_utils


def generate_catalogue(*, db) -> Catalogue:
    catalogue = {"hotels": crud_utils.read_all(model=Hotel, db_session=db)}
    rooms = crud_utils.read_all(model=Room, db_session=db)
    for hotel in catalogue["hotels"]:
        hotel.__dict__["rooms"] = []
        for room in rooms:
            if room.hotel_id == hotel.id:
                hotel.__dict__["rooms"].append(room.__dict__)
        for room in hotel.__dict__["rooms"]:
            room["categorie"] = crud_utils.read_one(
                model=Categorie, record_id=room["categorie_id"], db_session=db
            )
    catalogue["fluctuations"] = crud_utils.read_all(model=Fluctuation, db_session=db)
    return catalogue
