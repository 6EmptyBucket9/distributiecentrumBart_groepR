from sqlalchemy import Column, Integer, String
from app.models import db

class Locatie(db.Model):
    __tablename__ = 'locatie'

    idLocatie = Column(Integer, primary_key=True)
    locatie_naam = Column(String(45), nullable=False)