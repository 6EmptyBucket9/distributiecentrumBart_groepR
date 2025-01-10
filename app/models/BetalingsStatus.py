from sqlalchemy import Column, Integer, String
from app.models import db

class BetalingsStatus(db.Model):
    __tablename__ = 'betalings_status'
    idBetalings_status = Column(Integer, primary_key=True)
    status = Column(String(45), nullable=False)

    def get_idBetalings_status(self):
        return self.idBetalings_status

    def set_idBetalings_status(self, new_id):
        self.idBetalings_status = new_id

    def get_status(self):
        return self.status

    def set_status(self, new_status):
        self.status = new_status

    idBetalings_status = property(get_idBetalings_status, set_idBetalings_status)
    status = property(get_status, set_status)
