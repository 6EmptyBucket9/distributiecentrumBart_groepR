from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models import db
from app.models.Functies import Functies

class Medewerker(db.Model):
    __tablename__ = 'medewerker'

    Medewerkernr = Column(Integer, primary_key=True)
    voornaam = Column(String(45), nullable=False)
    tussenvoegsel = Column(String(45), nullable=True)
    achternaam = Column(String(45), nullable=False)
    telefoonnr = Column(String(45), nullable=False)
    functie = Column(Integer, ForeignKey('functies.ID'), nullable=False)
    in_dienst_sinds = Column(Date, nullable=False)

    functie_rel = db.relationship('Functies', backref='medewerkers', lazy='subquery')
