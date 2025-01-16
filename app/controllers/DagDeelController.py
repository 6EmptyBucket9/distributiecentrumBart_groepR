from app.models import db
from app.models.Dagdeel import Dagdeel

class DagdeelController:

    @staticmethod
    def get_all_dagdelen():
        """Get all Dagdeel entries."""
        return db.session.query(Dagdeel).all()

    @staticmethod
    def get_dagdeel_by_id(idDagdeel):
        """Get a Dagdeel entry by id."""
        return db.session.query(Dagdeel).filter_by(idDagdeel=idDagdeel).first()

    @staticmethod
    def create_dagdeel(dagdeel):
        """Create a new Dagdeel."""
        new_dagdeel = Dagdeel(dagdeel=dagdeel)
        db.session.add(new_dagdeel)
        db.session.commit()
        return new_dagdeel

    @staticmethod
    def update_dagdeel(idDagdeel, dagdeel):
        """Update an existing Dagdeel."""
        dagdeel_to_update = db.session.query(Dagdeel).filter_by(idDagdeel=idDagdeel).first()
        if dagdeel_to_update:
            dagdeel_to_update.dagdeel = dagdeel
            db.session.commit()
        return dagdeel_to_update

    @staticmethod
    def delete_dagdeel(idDagdeel):
        """Delete a Dagdeel."""
        dagdeel_to_delete = db.session.query(Dagdeel).filter_by(idDagdeel=idDagdeel).first()
        if dagdeel_to_delete:
            db.session.delete(dagdeel_to_delete)
            db.session.commit()
        return dagdeel_to_delete
