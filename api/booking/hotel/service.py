from ..hotel.model import Hotel, HotelCreate


def create(*, hotel_in: HotelCreate, db_session) -> Hotel:
    """Create a Hotel"""
    hotel = Hotel(**hotel_in.dict())
    db_session.add(hotel)
    db_session.commit()
    return hotel
