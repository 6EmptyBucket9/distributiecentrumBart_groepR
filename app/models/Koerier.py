from sqlalchemy import Column, Integer, String
from app.models import db

class Koerier(db.Model):
    __tablename__ = 'koerier'
    idKoerier = Column(Integer, primary_key=True)
    naam = Column(String(45), nullable=False)