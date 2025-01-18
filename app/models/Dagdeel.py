from sqlalchemy import Column, Integer, String
from app.models import db

class Dagdeel(db.Model):
    __tablename__ = 'dagdeel'
    idDagdeel = Column(Integer, primary_key=True)
    dagdeel = Column(String(45), nullable=False)