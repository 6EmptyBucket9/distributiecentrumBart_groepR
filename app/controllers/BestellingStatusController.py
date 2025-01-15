from app.models import db
from app.models.BestellingStatus import BestellingStatus

class BestellingStatusController:

    @staticmethod
    def get_all_bestellingstatus():
        """Get all BestellingStatus entries."""
        return db.session.query(BestellingStatus).all()

    @staticmethod
    def get_bestellingstatus_by_id(idBestelling_status):
        """Get a BestellingStatus entry by id."""
        return db.session.query(BestellingStatus).filter_by(idBestelling_status=idBestelling_status).first()

    @staticmethod
    def create_bestellingstatus(status):
        """Create a new BestellingStatus."""
        new_status = BestellingStatus(status=status)
        db.session.add(new_status)
        db.session.commit()
        return new_status

    @staticmethod
    def update_bestellingstatus(idBestelling_status, status):
        """Update an existing BestellingStatus."""
        status_to_update = db.session.query(BestellingStatus).filter_by(idBestelling_status=idBestelling_status).first()
        if status_to_update:
            status_to_update.status = status
            db.session.commit()
        return status_to_update

    @staticmethod
    def delete_bestellingstatus(idBestelling_status):
        """Delete a BestellingStatus."""
        status_to_delete = db.session.query(BestellingStatus).filter_by(idBestelling_status=idBestelling_status).first()
        if status_to_delete:
            db.session.delete(status_to_delete)
            db.session.commit()
        return status_to_delete
