def test_create_user(session):
    from booking.user.service import create
    from booking.user.model import UserCreate

    user_in = UserCreate(username="XXX", role=3, pwd_not_secure="mdp")
    user = create(user_in=user_in, db_session=session)
    assert user


def test_get_user(session, user):
    from booking.utils import crud_utils
    from booking.user.model import User

    user_out = crud_utils.read_one(model=User, record_id=user.id, db_session=session)
    assert user_out.id == user.id


def test_get_users(session, users):
    from booking.utils import crud_utils
    from booking.user.model import User

    users_out = crud_utils.read_all(model=User, db_session=session)
    assert len(users_out) == len(users)


def test_update_user(session, user):
    from booking.user.model import UserCreate, User
    from booking.utils import crud_utils

    user_in = UserCreate(username="XXX", role=3, pwd_not_secure="mdp")
    user_out = crud_utils.update(
        model=User, record=user_in, record_id=user.id, db_session=session
    )
    assert user_out.username == user.username
    assert user_out.role == user.role
    assert user_out.id == user.id


def test_delete_user(session, user):
    from booking.utils import crud_utils
    from booking.user.model import User

    resp = crud_utils.delete(model=User, record_id=user.id, db_session=session)
    assert resp == ("", 204)
