from sqlalchemy import Column, Integer, String
from app.models import db

class Functie(db.Model):
    __tablename__ = 'functies'
    ID = Column(Integer, primary_key=True)
    naam = Column(String(45), nullable=False)

    def get_id(self):
        return self.ID

    def set_id(self, new_id):
        self.ID = new_id

    def get_naam(self):
        return self.naam

    def set_naam(self, new_naam):
        self.naam = new_naam

    id = property(get_id, set_id)
    naam = property(get_naam, set_naam)
