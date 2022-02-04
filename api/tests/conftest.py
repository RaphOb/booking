from typing import List

import pytest
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.config import environ
from starlette.testclient import TestClient


environ["ENV"] = "test"
environ["SQL_DB_URI"] = "sqlite:///test_database?check_same_thread=False"
from booking.room.model import Room  # noqa
from booking.catalogue.model import Catalogue, HotelCatalogue, RoomCatalogue  # noqa
from booking.option.model import Option  # noqa
from booking.categorie.model import Categorie  # noqa
from booking.fluctuation.model import Fluctuation  # noqa
from booking.user.model import User  # noqa
from booking.config import SQL_DB_URI  # noqa
from booking.database import Base, engine, SessionLocal  # noqa
from booking import config  # noqa
from booking.main import app  # noqa
from booking.hotel.model import Hotel  # noqa

# set test config
from tests.factories import (
    HotelFactory,
    RoomFactory,
    CategorieFactory,
    ReservationFactory,
    FluctuationFactory,
    BillingFactory,
    OptionFactory,
    ReservationOptionFactory,
    UserFactory,
)  # noqa


@pytest.fixture(scope="session")
def db():
    if database_exists(SQL_DB_URI):
        drop_database(SQL_DB_URI)

    create_database(SQL_DB_URI)
    Base.metadata.create_all(engine)  # Create the tables.
    connection = engine.connect()
    yield connection
    connection.close()
    drop_database(SQL_DB_URI)


@pytest.fixture(scope="function")
def session(db):
    """
    Creates a new database session (with working transaction)
    for test duration.
    """
    transaction = db.begin()
    session = SessionLocal(bind=db)
    # we need factories to use same session as tests
    HotelFactory._meta.sqlalchemy_session = session
    RoomFactory._meta.sqlalchemy_session = session
    CategorieFactory._meta.sqlalchemy_session = session
    ReservationFactory._meta.sqlalchemy_session = session
    FluctuationFactory._meta.sqlalchemy_session = session
    UserFactory._meta.sqlalchemy_session = session
    BillingFactory._meta.sqlalchemy_session = session
    OptionFactory._meta.sqlalchemy_session = session
    ReservationOptionFactory._meta.sqlalchemy_session = session

    yield session
    session.close()
    transaction.rollback()


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture()
def room(session):
    return RoomFactory()


@pytest.fixture()
def rooms(session):
    return [RoomFactory(), RoomFactory()]


@pytest.fixture()
def categorie(session):
    return CategorieFactory()


@pytest.fixture()
def categories(session):
    return [CategorieFactory(), CategorieFactory()]


@pytest.fixture()
def hotel(session):
    return HotelFactory()


@pytest.fixture()
def hotels(session) -> List[Hotel]:
    return [HotelFactory(), HotelFactory()]


@pytest.fixture()
def reservation(session):
    return ReservationFactory()


@pytest.fixture()
def reservations(session):
    return [ReservationFactory(), ReservationFactory()]


@pytest.fixture()
def fluctuation(session):
    return FluctuationFactory()


@pytest.fixture()
def fluctuations(session):
    return [FluctuationFactory(), FluctuationFactory()]


@pytest.fixture()
def billing(session):
    return BillingFactory()


@pytest.fixture()
def billings(session):
    return [BillingFactory(), BillingFactory()]


@pytest.fixture()
def option(session):
    return OptionFactory()


@pytest.fixture()
def options(session):
    return [OptionFactory(), OptionFactory()]


@pytest.fixture()
def reservation_option(session):
    return ReservationOptionFactory()


@pytest.fixture(scope="function")
def user():
    return UserFactory()


@pytest.fixture(scope="function")
def users():
    return [UserFactory(), UserFactory()]


@pytest.fixture()
def reservation_options(session):
    return [ReservationOptionFactory(), ReservationOptionFactory()]


@pytest.fixture
def mock_hotels(mocker, hotels) -> List[Hotel]:
    mocker.patch("booking.hotel.view.crud_utils.read_all", return_value=hotels)
    mocker.patch("booking.hotel.view.crud_utils.read_one", return_value=hotels[0])
    mocker.patch("booking.hotel.view.create", return_value=hotels[0])
    mocker.patch("booking.hotel.view.crud_utils.update", return_value=hotels[0])
    mocker.patch("booking.hotel.view.crud_utils.delete")
    return hotels


@pytest.fixture()
def mock_fluctuations(mocker, fluctuations) -> List[Fluctuation]:
    mocker.patch(
        "booking.fluctuation.view.crud_utils.read_all", return_value=fluctuations
    )
    mocker.patch(
        "booking.fluctuation.view.crud_utils.read_one", return_value=fluctuations[0]
    )
    mocker.patch("booking.fluctuation.view.create", return_value=fluctuations[0])
    mocker.patch(
        "booking.fluctuation.view.crud_utils.update", return_value=fluctuations[0]
    )
    mocker.patch("booking.fluctuation.view.crud_utils.delete")
    return fluctuations


@pytest.fixture()
def mock_categories(mocker, categories) -> List[Categorie]:
    mocker.patch("booking.categorie.view.crud_utils.read_all", return_value=categories)
    mocker.patch(
        "booking.categorie.view.crud_utils.read_one", return_value=categories[0]
    )
    mocker.patch("booking.categorie.view.create", return_value=categories[0])
    mocker.patch("booking.categorie.view.crud_utils.update", return_value=categories[0])
    mocker.patch("booking.categorie.view.crud_utils.delete")
    return categories


@pytest.fixture()
def mock_options(mocker, options) -> List[Option]:
    mocker.patch("booking.option.view.crud_utils.read_all", return_value=options)
    mocker.patch("booking.option.view.crud_utils.read_one", return_value=options[0])
    mocker.patch("booking.option.view.create", return_value=options[0])
    mocker.patch("booking.option.view.crud_utils.update", return_value=options[0])
    mocker.patch("booking.option.view.crud_utils.delete")
    return options


@pytest.fixture()
def mock_rooms(mocker, rooms) -> List[Room]:
    mocker.patch("booking.room.view.crud_utils.read_all", return_value=rooms)
    mocker.patch("booking.room.view.crud_utils.read_one", return_value=rooms[0])
    mocker.patch("booking.room.view.create", return_value=rooms[0])
    mocker.patch("booking.room.view.crud_utils.update", return_value=rooms[0])
    mocker.patch("booking.room.view.crud_utils.delete")
    return rooms


@pytest.fixture
def mock_hotels_not_found(mocker):
    mocker.patch("booking.hotel.get", return_value=None)
    mocker.patch("booking.hotel.update_hotel", return_value=None)


@pytest.fixture
def mock_users(mocker, users) -> List[User]:
    mocker.patch("booking.user.view.crud_utils.read_all", return_value=users)
    mocker.patch("booking.user.view.crud_utils.read_one", return_value=users[0])
    mocker.patch("booking.user.view.create", return_value=users[0])
    mocker.patch("booking.user.view.crud_utils.update", return_value=users[0])
    mocker.patch("booking.user.view.crud_utils.delete")
    return users


@pytest.fixture
def mock_agendas(mocker):
    mocker.patch("booking.agendas.view.generate_agendas", return_value={})


@pytest.fixture
def mock_catalogue(mocker, hotels, fluctuations, rooms, categorie):
    mocker.patch(
        "booking.catalogue.view.generate_catalogue",
        return_value=Catalogue(
            hotels=HotelCatalogue(
                rooms=[RoomCatalogue(categorie=categorie, number=10)]
            ),
            fluctuations=fluctuations,
        ),
    )
