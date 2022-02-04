from ..option.model import Option, OptionCreate


def create(*, option_in: OptionCreate, db_session):
    option = Option(**option_in.dict())
    db_session.add(option)
    db_session.commit()
    return option
