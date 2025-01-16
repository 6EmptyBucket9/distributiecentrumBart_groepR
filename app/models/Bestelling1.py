from sqlalchemy import Column, Integer, Date, ForeignKey, SmallInteger
from sqlalchemy import func
from app.models import db

# Import the related models for the relationships
from app.models.Medewerker import Medewerker
from app.models.BestellingStatus import BestellingStatus
from app.models.Levermoment import Levermoment
from app.models.Dagdeel import Dagdeel
from app.models.Koerier import Koerier
from app.models.ProductInBestelling import ProductInBestelling
from app.models.Klant import Klant  # Ensure to import the Klant model

from sqlalchemy import Column, Integer, Date, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models import db
from app.models.Klant import Klant

class Bestelling(db.Model):
    __tablename__ = 'bestelling'

    bestellingsnr = Column(Integer, primary_key=True)
    klantnr = Column(Integer, ForeignKey('klant.klantnr'), nullable=False)
    klant_rel = relationship('Klant', backref='bestellingen')
    bestelling_medewerker = Column(Integer, ForeignKey('medewerker.Medewerkernr'), nullable=False)
    datum = Column(Date, nullable=False)
    status = Column(Integer, ForeignKey('bestelling_status.idBestelling_status'), nullable=False)
    bestelling_levermoment = Column(Integer, ForeignKey('levermoment.idLevermoment'), nullable=False)
    bestelling_dagdeel = Column(Integer, ForeignKey('dagdeel.idDagdeel'), nullable=False)
    bestelling_koerier = Column(Integer, ForeignKey('koerier.idKoerier'), nullable=False)
    km_transport = Column(Integer, nullable=False)
    spoed = Column(SmallInteger, nullable=False)
    # Define the relationships to the related models
    medewerker_rel = db.relationship('Medewerker', backref='bestellingen')
    status_rel = db.relationship('BestellingStatus', backref='bestellingen')
    levermoment_rel = db.relationship('Levermoment', backref='bestellingen')
    dagdeel_rel = db.relationship('Dagdeel', backref='bestellingen')
    koerier_rel = db.relationship('Koerier', backref='bestellingen')
    products = db.relationship('ProductInBestelling', backref='bestelling')

    # Computed property for totaalbedrag
    @property
    def totaalbedrag(self):
        total = db.session.query(func.sum(ProductInBestelling.prijs * ProductInBestelling.aantal)) \
            .filter(ProductInBestelling.bestelling_id == self.bestellingsnr) \
            .scalar()
        return total or 0  # return 0 if the result is None
