
from sqlalchemy import Column, Integer, String
from app.models import db

class BestellingStatus(db.Model):
    __tablename__ = 'bestelling_status'

    idBestelling_status = Column(Integer, primary_key=True)
    status = Column(String(45), nullable=False)
