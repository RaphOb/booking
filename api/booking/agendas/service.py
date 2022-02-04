from datetime import timedelta

from ..agendas.model import Agendas
from ..hotel.model import Hotel
from ..room.service import if_reserved
from ..utils import crud_utils


# On*m*d
def generate_agendas(*, agenda_in: Agendas, db_session):
    res = {}
    start = agenda_in.start
    end = agenda_in.end
    delta = timedelta(days=1)

    hotels = crud_utils.read_all(model=Hotel, db_session=db_session)
    # get les hotels
    for hotel in hotels:
        res[hotel.name] = []
        # get les rooms de hotel
        for room in hotel.rooms:
            r = {room.number: []}
            start_res = start
            # boucle sur toutes les dates entre start et end
            while start_res <= end:
                # Check si pas de reservation à cette date
                is_reserved = if_reserved(
                    room_number=room.number, date=start_res, db_session=db_session
                )
                # si pas de resultat, room dispo on ajoute au resultat
                if not is_reserved:
                    r[room.number].append(start_res)

                # ajoute un jour à start_res
                start_res += delta
            res[hotel.name].append(r)
    return res
