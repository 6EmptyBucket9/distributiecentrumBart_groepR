from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models import db
from app.models.Medewerker import Medewerker
from app.models.Klant import Klant
from app.models.Bestelling import Bestelling
from app.models.BetalingsStatus import BetalingsStatus

class Factuur(db.Model):
    __tablename__ = 'factuur'

    factuurnr = Column(Integer, primary_key=True)
    factuur_medewerker = Column(Integer, ForeignKey('medewerker.Medewerkernr'), nullable=False)
    factuur_klant = Column(Integer, ForeignKey('klant.klantnr'), nullable=False)
    factuur_bestelling = Column(Integer, ForeignKey('bestelling.bestellingsnr'), nullable=False)
    datum_uitgifte = Column(Date, nullable=False)
    verval_datum = Column(Date, nullable=False)
    betaling_status = Column(Integer, ForeignKey('betalings_status.idBetalings_status'), nullable=False)

    medewerker_rel = db.relationship('Medewerker', backref='facturen')
    klant_rel = db.relationship('Klant', backref='facturen')
    bestelling_rel = db.relationship('Bestelling', backref='facturen')
    betalings_status_rel = db.relationship('BetalingsStatus', backref='facturen')
