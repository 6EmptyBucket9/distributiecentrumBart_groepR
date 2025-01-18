from sqlalchemy import Column, Integer, String
from app.models import db

class Functies(db.Model):
    __tablename__ = 'functies'
    ID = Column(Integer, primary_key=True)
    naam = Column(String(45), nullable=False)