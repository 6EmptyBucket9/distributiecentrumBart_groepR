from sqlalchemy import Column, Integer, String
from app.models import db

class Fabrikant(db.Model):
    __tablename__ = 'fabrikant'

    idFabrikant = Column(Integer, primary_key=True)
    naam = Column(String(45), nullable=False)
    emailadres = Column(String(45), nullable=False)
    telefoonnr = Column(String(45), nullable=False)
