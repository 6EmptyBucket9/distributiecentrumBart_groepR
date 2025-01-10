from sqlalchemy import Column, Integer, String
from app.models import db

class BetalingsStatus(db.Model):
    __tablename__ = 'betalings_status'

    idBetalings_status = Column(Integer, primary_key=True)
    status = Column(String(45), nullable=False)
