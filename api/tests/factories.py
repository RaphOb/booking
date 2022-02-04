import uuid
from datetime import datetime

import factory
from factory import LazyAttribute
from pytz import UTC
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import (
    FuzzyDateTime,
    FuzzyText,
    FuzzyInteger,
    FuzzyChoice,
    FuzzyFloat,
)

from booking.billing.model import Billing
from booking.categorie.model import Categorie
from booking.fluctuation.model import Fluctuation
from booking.hotel.model import Hotel
from booking.option.model import Option
from booking.reservation.model import Reservation
from booking.reservation_option.model import ReservationOption
from booking.room.model import Room
from booking.user.model import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory"""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session_persistence = "flush"


class TimeStampBaseFactory(BaseFactory):
    """Timestamp Base Factory."""

    created_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))
    updated_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))


class HotelFactory(BaseFactory):
    """Hotel Factory"""

    name = FuzzyText()
    city = FuzzyText()
    street = FuzzyText()
    nb_room = FuzzyInteger(10)
    nb_park = FuzzyInteger(10)
    nb_bb = FuzzyInteger(10)

    @factory.post_generation
    def rooms(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for _ in range(extracted):
                RoomFactory(hotel_id=self.id)
        else:
            import random

            number_of_units = random.randint(1, 10)
            for n in range(number_of_units):
                RoomFactory(hotel_id=self.id)

    class Meta:
        """Factory configuration"""

        model = Hotel


class CategorieFactory(BaseFactory):
    """Categorie factory"""

    type = FuzzyChoice([1, 2, 3, 4, 5])
    base_price = FuzzyFloat(2000)
    max_people = FuzzyInteger(10)

    @factory.post_generation
    def rooms(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for _ in range(extracted):
                RoomFactory()
        else:
            import random

            number_of_units = random.randint(1, 10)
            for n in range(number_of_units):
                RoomFactory()

    class Meta:
        model = Categorie


class RoomFactory(BaseFactory):
    """Room Factory"""

    hotel_id = LazyAttribute(lambda _: str(uuid.uuid4()))
    categorie_id = LazyAttribute(lambda _: str(uuid.uuid4()))
    number = factory.Sequence(int)

    class Meta:
        model = Room


class ReservationFactory(BaseFactory):
    """Reservation Factory"""

    start_res = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))
    end_res = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))
    name_res = FuzzyText()
    phone_res = FuzzyText()
    nb_people = FuzzyInteger(1, 10)

    @factory.post_generation
    def bill(self, create, extracted, **kwargs):
        if not create:
            return
        else:
            BillingFactory(reservation_id=self.id)

    @factory.post_generation
    def reservation_option(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for _ in range(extracted):
                ReservationOptionFactory()
        else:
            import random

            number_of_units = random.randint(1, 10)
            for n in range(number_of_units):
                ReservationOptionFactory()

    class Meta:
        model = Reservation


class FluctuationFactory(BaseFactory):
    """Fluctuation Factory"""

    condition = FuzzyChoice([1, 2, 3, 4, 5, 6, 7, 8])
    rate = FuzzyFloat(-1, 1)

    class Meta:
        model = Fluctuation


class BillingFactory(BaseFactory):
    """Billing Factory"""

    reservation_id = LazyAttribute(lambda _: str(uuid.uuid4()))
    bill = FuzzyFloat(1, 10000)
    has_payed = FuzzyChoice([False, True])

    class Meta:
        model = Billing


class OptionFactory(BaseFactory):
    name = FuzzyText()
    price = FuzzyFloat(1, 1000)
    delay_before = FuzzyInteger(10)

    @factory.post_generation
    def reservation_option(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for _ in range(extracted):
                ReservationOptionFactory()
        else:
            import random

            number_of_units = random.randint(1, 10)
            for n in range(number_of_units):
                ReservationOptionFactory()

    class Meta:
        model = Option


class UserFactory(BaseFactory):
    username = FuzzyText()
    role = FuzzyChoice([1, 2, 3])
    pwd_secure = FuzzyText()

    class Meta:
        model = User


class ReservationOptionFactory(BaseFactory):
    reservation_id = LazyAttribute(lambda _: str(uuid.uuid4()))
    option_id = LazyAttribute(lambda _: str(uuid.uuid4()))
    nb_days = FuzzyInteger(10)

    class Meta:
        model = ReservationOption
