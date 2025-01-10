from sqlalchemy import Column, Integer, String
from app.models import db

class Koerier(db.Model):
    __tablename__ = 'koerier'
    idKoerier = Column(Integer, primary_key=True)
    naam = Column(String(45), nullable=False)

    def get_idKoerier(self):
        return self.idKoerier

    def set_idKoerier(self, new_id):
        self.idKoerier = new_id

    def get_naam(self):
        return self.naam

    def set_naam(self, new_naam):
        self.naam = new_naam

    idKoerier = property(get_idKoerier, set_idKoerier)
    naam = property(get_naam, set_naam)
