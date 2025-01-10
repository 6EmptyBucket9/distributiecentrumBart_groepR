from sqlalchemy import Column, Integer, String
from app.models import db

class BestellingStatus(db.Model):
    __tablename__ = 'bestelling_status'
    idBestelling_status = Column(Integer, primary_key=True)
    status = Column(String(45), nullable=False)

    def get_idBestelling_status(self):
        return self.idBestelling_status

    def set_idBestelling_status(self, new_id):
        self.idBestelling_status = new_id

    def get_status(self):
        return self.status

    def set_status(self, new_status):
        self.status = new_status

    idBestelling_status = property(get_idBestelling_status, set_idBestelling_status)
    status = property(get_status, set_status)
