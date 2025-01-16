from app.models import db
from app.models.Koerier import Koerier

class KoerierController:

    @staticmethod
    def create_koerier(koerier_data):
        """Create a new koerier."""
        new_koerier = Koerier(
            naam=koerier_data['naam']
        )
        db.session.add(new_koerier)
        db.session.commit()
        return new_koerier

    @staticmethod
    def get_all_koeriers():
        """Get all koeriers."""
        return db.session.query(Koerier).all()

    @staticmethod
    def get_koerier_by_id(koerier_id):
        """Get a koerier by ID."""
        return db.session.query(Koerier).filter_by(idKoerier=koerier_id).first()

    @staticmethod
    def update_koerier(koerier, koerier_data):
        """Update an existing koerier."""
        koerier.naam = koerier_data['naam']
        db.session.commit()
        return koerier

    @staticmethod
    def delete_koerier(koerier):
        """Delete a koerier."""
        db.session.delete(koerier)
        db.session.commit()
