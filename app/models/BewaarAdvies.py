from sqlalchemy import Column, Integer, String
from app.models import db

class BewaarAdvies(db.Model):
    __tablename__ = 'bewaar_advies'

    idBewaar_advies = Column(Integer, primary_key=True)
    advies = Column(String(45), nullable=False)
