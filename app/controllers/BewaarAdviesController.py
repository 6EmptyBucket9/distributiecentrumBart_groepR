from app.models import db
from app.models.BewaarAdvies import BewaarAdvies

class BewaarAdviesController:

    @staticmethod
    def get_all_bewaaradviezen():
        """Get all BewaarAdvies entries."""
        return db.session.query(BewaarAdvies).all()

    @staticmethod
    def get_bewaaradvies_by_id(idBewaar_advies):
        """Get a BewaarAdvies entry by id."""
        return db.session.query(BewaarAdvies).filter_by(idBewaar_advies=idBewaar_advies).first()

    @staticmethod
    def create_bewaaradvies(advies):
        """Create a new BewaarAdvies."""
        new_advies = BewaarAdvies(advies=advies)
        db.session.add(new_advies)
        db.session.commit()
        return new_advies

    @staticmethod
    def update_bewaaradvies(idBewaar_advies, advies):
        """Update an existing BewaarAdvies."""
        advies_to_update = db.session.query(BewaarAdvies).filter_by(idBewaar_advies=idBewaar_advies).first()
        if advies_to_update:
            advies_to_update.advies = advies
            db.session.commit()
        return advies_to_update

    @staticmethod
    def delete_bewaaradvies(idBewaar_advies):
        """Delete a BewaarAdvies."""
        advies_to_delete = db.session.query(BewaarAdvies).filter_by(idBewaar_advies=idBewaar_advies).first()
        if advies_to_delete:
            db.session.delete(advies_to_delete)
            db.session.commit()
        return advies_to_delete
