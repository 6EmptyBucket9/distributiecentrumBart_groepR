from app.models import db
from app.models.BetalingsStatus import BetalingsStatus

class BetalingsStatusController:

    @staticmethod
    def get_all_betalingsstatus():
        """Get all BetalingsStatus entries."""
        return db.session.query(BetalingsStatus).all()

    @staticmethod
    def get_betalingsstatus_by_id(idBetalings_status):
        """Get a BetalingsStatus entry by id."""
        return db.session.query(BetalingsStatus).filter_by(idBetalings_status=idBetalings_status).first()

    @staticmethod
    def create_betalingsstatus(status):
        """Create a new BetalingsStatus."""
        new_status = BetalingsStatus(status=status)
        db.session.add(new_status)
        db.session.commit()
        return new_status

    @staticmethod
    def update_betalingsstatus(idBetalings_status, status):
        """Update an existing BetalingsStatus."""
        status_to_update = db.session.query(BetalingsStatus).filter_by(idBetalings_status=idBetalings_status).first()
        if status_to_update:
            status_to_update.status = status
            db.session.commit()
        return status_to_update

    @staticmethod
    def delete_betalingsstatus(idBetalings_status):
        """Delete a BetalingsStatus."""
        status_to_delete = db.session.query(BetalingsStatus).filter_by(idBetalings_status=idBetalings_status).first()
        if status_to_delete:
            db.session.delete(status_to_delete)
            db.session.commit()
        return status_to_delete
