from app.models import db
from app.models.Medewerker import Medewerker  # Adjust import as per your project structure

class MedewerkerController:

    @staticmethod
    def create_medewerker(medewerker_data):
        """Create a new medewerker."""
        new_medewerker = Medewerker(
            voornaam=medewerker_data['voornaam'],
            tussenvoegsel=medewerker_data['tussenvoegsel'],
            achternaam=medewerker_data['achternaam'],
            telefoonnr=medewerker_data['telefoonnr'],
            functie=medewerker_data['functie'],
            in_dienst_sinds=medewerker_data['in_dienst_sinds']
        )
        db.session.add(new_medewerker)
        db.session.commit()
        return new_medewerker

    @staticmethod
    def get_all_medewerkers():
        """Get all medewerkers."""
        return db.session.query(Medewerker).all()

    @staticmethod
    def get_medewerker_by_id(medewerkernr):
        """Get a medewerker by ID."""
        return db.session.query(Medewerker).filter_by(Medewerkernr=medewerkernr).first()

    @staticmethod
    def update_medewerker(medewerker, medewerker_data):
        """Update an existing medewerker."""
        medewerker.voornaam = medewerker_data['voornaam']
        medewerker.tussenvoegsel = medewerker_data['tussenvoegsel']
        medewerker.achternaam = medewerker_data['achternaam']
        medewerker.telefoonnr = medewerker_data['telefoonnr']
        medewerker.functie = medewerker_data['functie']
        medewerker.in_dienst_sinds = medewerker_data['in_dienst_sinds']
        
        db.session.commit()
        return medewerker

    @staticmethod
    def delete_medewerker(medewerker):
        """Delete a medewerker."""
        db.session.delete(medewerker)
        db.session.commit()
