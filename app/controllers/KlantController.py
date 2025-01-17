from app.models import db
from app.models.Klant import Klant

class KlantController:
    
    @staticmethod
    def get_all_klanten():
        """Fetch all klanten from the database."""
        return Klant.query.all()
    
    @staticmethod
    def get_klant_by_id(klantnr):
        """Fetch a klant by klantnr."""
        return Klant.query.get(klantnr)
    
    @staticmethod
    def create_klant(form_data):
        """Create a new klant using form data."""
        new_klant = Klant(
            voornaam=form_data['voornaam'],
            tussenvoegsel=form_data.get('tussenvoegsel'),
            achternaam=form_data['achternaam'],
            telefoonnr=form_data['telefoonnr']
        )
        db.session.add(new_klant)
        db.session.commit()
        return new_klant
    
    @staticmethod
    def update_klant(klant, form_data):
        """Update an existing klant's data."""
        klant.voornaam = form_data['voornaam']
        klant.tussenvoegsel = form_data.get('tussenvoegsel')
        klant.achternaam = form_data['achternaam']
        klant.telefoonnr = form_data['telefoonnr']
        
        db.session.commit()
        return klant
    
    @staticmethod
    def delete_klant(klant):
        """Delete a klant from the database."""
        db.session.delete(klant)
        db.session.commit()
