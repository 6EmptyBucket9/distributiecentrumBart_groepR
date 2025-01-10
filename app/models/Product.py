from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models import db
from app.models.BewaarAdvies import BewaarAdvies
from app.models.Fabrikant import Fabrikant
from app.models.Locatie import Locatie

class Product(db.Model):
    __tablename__ = 'product'

    productnr = Column(Integer, primary_key=True)
    naam = Column(String(45), nullable=False)
    bederfelijkheidsfactor = Column(Integer, nullable=False)
    batchnummer = Column(Integer, nullable=False)
    verpakkingsgrote = Column(Integer, nullable=False)
    locatie_id = Column(Integer, ForeignKey('locatie.idLocatie'), nullable=False)
    voorraad = Column(Integer, nullable=False)
    verschil_in_voorraad = Column(Integer, nullable=False)
    bewaaradvies = Column(Integer, ForeignKey('bewaar_advies.idBewaar_advies'), nullable=False)
    product_fabrikant = Column(Integer, ForeignKey('fabrikant.idFabrikant'), nullable=False)

    locatie_rel = db.relationship('Locatie', backref='producten')
    bewaaradvies_rel = db.relationship('BewaarAdvies', backref='producten')
    fabrikant_rel = db.relationship('Fabrikant', backref='producten')

