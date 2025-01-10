from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models import db
from app.models.Functies import Functie

class Medewerker(db.Model):
    __tablename__ = 'medewerker'
    Medewerkernr = Column(Integer, primary_key=True)
    voornaam = Column(String(45), nullable=False)
    tussenvoegsel = Column(String(45), nullable=True)
    achternaam = Column(String(45), nullable=False)
    telefoonnr = Column(String(45), nullable=False)
    functie = Column(Integer, ForeignKey('functies.ID'), nullable=False)
    in_dienst_sinds = Column(Date, nullable=False)

    functie_rel = relationship('Functie', backref='medewerkers')

    def get_medewerkernr(self):
        return self.Medewerkernr

    def set_medewerkernr(self, new_nr):
        self.Medewerkernr = new_nr

    def get_voornaam(self):
        return self.voornaam

    def set_voornaam(self, new_voornaam):
        self.voornaam = new_voornaam

    def get_achternaam(self):
        return self.achternaam

    def set_achternaam(self, new_achternaam):
        self.achternaam = new_achternaam

    medewerkernr = property(get_medewerkernr, set_medewerkernr)
    voornaam = property(get_voornaam, set_voornaam)
    achternaam = property(get_achternaam, set_achternaam)
