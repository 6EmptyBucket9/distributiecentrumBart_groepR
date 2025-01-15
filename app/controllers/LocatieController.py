from app.models import db
from app.models.Locatie import Locatie

class LocatieController:

    @staticmethod
    def get_all_locaties():
        """Get all locaties."""
        return db.session.query(Locatie).all()

    @staticmethod
    def get_locatie_by_id(locatie_id):
        """Get a locatie by id."""
        return db.session.query(Locatie).filter_by(id=locatie_id).first()
