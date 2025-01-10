from sqlalchemy import Column, Integer, String
from app.models import db

class Klant(db.Model):
    __tablename__ = 'klant'

    klantnr = Column(Integer, primary_key=True)
    voornaam = Column(String(45), nullable=False)
    tussenvoegsel = Column(String(45), nullable=True)
    achternaam = Column(String(45), nullable=False)
    telefoonnr = Column(String(45), nullable=False)
