from app.controllers import ProductInBestellingController
from app.models import db
from app.models.Bestelling import Bestelling
from app.models.BestellingStatus import BestellingStatus
from app.models.Product import Product
from app.models.ProductInBestelling import ProductInBestelling
from app.models.Medewerker import Medewerker
from app.models.Koerier import Koerier
from app.models.Levermoment import Levermoment
from app.models.Dagdeel import Dagdeel
from app.utils import generate_track_and_trace_code



class BestellingController:

    @staticmethod
    def get_bestelling_by_nr(bestelling_bestellingsnr):
        """Fetch bestelling by ID."""
        return db.session.query(Bestelling).filter_by(bestellingsnr=bestelling_bestellingsnr).first()

    @staticmethod
    def get_all_bestellingen():
        """Fetch all bestellingen, with optional filters."""
        bestellingen = db.session.query(Bestelling)
        return bestellingen
    
    @staticmethod
    def get_bestelling_by_status(status=None):
        query = db.session.query(Bestelling)  # Initialize the query object

        if status:
            query = query.filter(Bestelling.status == status)

        return query


    @staticmethod
    def update_bestelling_status(bestelling, status):
        """Update bestelling status."""
        bestelling.status = status
        db.session.commit()

    @staticmethod
    def update_bestelling_levermoment(bestelling, levermoment):
        """Update bestelling levermoment."""
        bestelling.bestelling_levermoment = levermoment
        db.session.commit()

    @staticmethod
    def update_bestelling_dagdeel(bestelling, dagdeel):
        """Update bestelling status."""
        bestelling.bestelling_dagdeel = dagdeel
        db.session.commit()

    @staticmethod
    def create_new_bestelling(form_data):
        """Create a new bestelling."""
        new_bestelling = Bestelling(
            bestelling_medewerker=form_data['bestelling_medewerker'],
            datum=form_data['datum'],
            status=form_data['status'],
            bestelling_levermoment=form_data['bestelling_levermoment'],
            bestelling_dagdeel=form_data['bestelling_dagdeel'],
            bestelling_koerier=form_data['bestelling_koerier'],
            km_transport=form_data['km_transport'],
            spoed=form_data['spoed']
        )
        db.session.add(new_bestelling)
        db.session.commit()

        return new_bestelling

    @staticmethod
    def generate_track_code():
        """Generate track and trace code."""
        return generate_track_and_trace_code()

    @staticmethod
    def get_related_models():
        """Fetch all related models."""
        return {
            'products': db.session.query(Product).all(),
            'medewerkers': db.session.query(Medewerker).all(),
            'koeriers': db.session.query(Koerier).all(),
            'levermomenten': db.session.query(Levermoment).all(),
            'dagdelen': db.session.query(Dagdeel).all(),
            'statuses': db.session.query(BestellingStatus).all()
        }


