from app.models import db
from app.models.Fabrikant import Fabrikant

class FabrikantController:

    @staticmethod
    def get_all_fabrikanten():
        """Get all Fabrikant entries."""
        return db.session.query(Fabrikant).all()

    @staticmethod
    def get_fabrikant_by_id(idFabrikant):
        """Get a Fabrikant entry by id."""
        return db.session.query(Fabrikant).filter_by(idFabrikant=idFabrikant).first()

    @staticmethod
    def create_fabrikant(naam, emailadres, telefoonnr):
        """Create a new Fabrikant."""
        new_fabrikant = Fabrikant(naam=naam, emailadres=emailadres, telefoonnr=telefoonnr)
        db.session.add(new_fabrikant)
        db.session.commit()
        return new_fabrikant

    @staticmethod
    def update_fabrikant(idFabrikant, naam, emailadres, telefoonnr):
        """Update an existing Fabrikant."""
        fabrikant_to_update = db.session.query(Fabrikant).filter_by(idFabrikant=idFabrikant).first()
        if fabrikant_to_update:
            fabrikant_to_update.naam = naam
            fabrikant_to_update.emailadres = emailadres
            fabrikant_to_update.telefoonnr = telefoonnr
            db.session.commit()
        return fabrikant_to_update

    @staticmethod
    def delete_fabrikant(idFabrikant):
        """Delete a Fabrikant."""
        fabrikant_to_delete = db.session.query(Fabrikant).filter_by(idFabrikant=idFabrikant).first()
        if fabrikant_to_delete:
            db.session.delete(fabrikant_to_delete)
            db.session.commit()
        return fabrikant_to_delete
