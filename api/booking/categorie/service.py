from .model import CategorieCreate, Categorie


def create(*, categorie_in: CategorieCreate, db_session) -> Categorie:
    """Create Categorie"""
    categorie_dict = categorie_in.dict()
    # TODO add room
    categorie = Categorie(**categorie_dict)
    db_session.add(categorie)
    db_session.commit()
    return categorie
