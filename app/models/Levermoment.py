from sqlalchemy import Column, Integer, String
from app.models import db

class Levermoment(db.Model):
    __tablename__ = 'levermoment'
    idLevermoment = Column(Integer, primary_key=True)
    moment = Column(String(45), nullable=False)

    def get_idLevermoment(self):
        return self.idLevermoment

    def set_idLevermoment(self, new_id):
        self.idLevermoment = new_id

    def get_moment(self):
        return self.moment

    def set_moment(self, new_moment):
        self.moment = new_moment

    idLevermoment = property(get_idLevermoment, set_idLevermoment)
    moment = property(get_moment, set_moment)
