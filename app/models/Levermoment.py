from sqlalchemy import Column, Integer, String
from app.models import db

class Levermoment(db.Model):
    __tablename__ = 'levermoment'
    idLevermoment = Column(Integer, primary_key=True)
    moment = Column(String(45), nullable=False)
