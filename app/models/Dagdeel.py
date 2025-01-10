from sqlalchemy import Column, Integer, String
from app.models import db

class Dagdeel(db.Model):
    __tablename__ = 'dagdeel'
    idDagdeel = Column(Integer, primary_key=True)
    dagdeel = Column(String(45), nullable=False)

    def get_idDagdeel(self):
        return self.idDagdeel

    def set_idDagdeel(self, new_id):
        self.idDagdeel = new_id

    def get_dagdeel(self):
        return self.dagdeel

    def set_dagdeel(self, new_dagdeel):
        self.dagdeel = new_dagdeel

    idDagdeel = property(get_idDagdeel, set_idDagdeel)
    dagdeel = property(get_dagdeel, set_dagdeel)
