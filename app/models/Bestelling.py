from sqlalchemy import Column, Integer, Date, ForeignKey, SmallInteger
from app.models import db

# Import the related models for the relationships
from app.models.Medewerker import Medewerker
from app.models.BestellingStatus import BestellingStatus
from app.models.Levermoment import Levermoment
from app.models.Dagdeel import Dagdeel
from app.models.Koerier import Koerier
from app.models.ProductInBestelling import ProductInBestelling

class Bestelling(db.Model):
    __tablename__ = 'bestelling'

    bestellingsnr = Column(Integer, primary_key=True)
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
